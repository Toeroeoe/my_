


def save_png(fig, name_file: str, bbox_inches: str = 'tight', dpi: int = 300, transparent: bool = False):
    
    fig.savefig(name_file, bbox_inches = bbox_inches, dpi = dpi, transparent = transparent)



def save_pdf(pdf, fig):
    
    import matplotlib.pyplot as plt

    pdf.savefig(fig)
    plt.close()