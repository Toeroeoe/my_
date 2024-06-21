
import numpy as np

from sklearn.cluster import KMeans, DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score

def kmeans(data: list[np.ndarray],
           n_clusters: int | list[int]):
    
    if isinstance(n_clusters, int): n_clusters = [n_clusters]#

    print(f'\nCompute kmeans clusters (N = {n_clusters})...\n')
    
    data_stacked = np.stack(data, axis = -1)
    data_valid = ~np.isnan(data_stacked)

    mask = np.all(data_valid, axis = -1)

    data_masked = data_stacked[mask]
    
    labels = []
    centroids = []
    scores = []

    for i, nc in enumerate(n_clusters):

        kmeans = KMeans(n_clusters = nc)
        labels.append(kmeans.fit_predict(data_masked))
        centroids.append(kmeans.cluster_centers_)

        scores.append(silhouette_score(data_masked, 
                                        labels[i]))
            
        print(f'\nFor n_clusters = {nc}, silhouette score is {scores[i]}...\n')
    
    i_opt = np.argmax(scores)
    
    labels_opt = labels[i_opt]
    centroids_opt = centroids[i_opt]
    scores_opt = scores[i_opt]

    return labels_opt, centroids_opt, scores_opt


def dbscan(data: list[np.ndarray],
           **kwargs):
    
    from joblib import effective_n_jobs
    
    print(f'\nCompute DBscan clusters')
    print(f'with {effective_n_jobs(-1)} cpus...\n')

    shape = data[0].shape
    
    data_stacked = np.stack(data, axis = -1)
    data_valid = ~np.isnan(data_stacked)

    mask = np.all(data_valid, axis = -1)

    data_masked = data_stacked[mask]

    db = DBSCAN(**kwargs, n_jobs = -1)  
    labels = db.fit_predict(data_masked)

    array_r = np.zeros(shape)
    array_r[:] = np.nan
    array_r[mask] = labels

    return array_r


