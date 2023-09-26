


def save_png(fig, name_file: str, bbox_inches: str = 'tight', dpi: int = 300):
    
    fig.savefig(name_file, bbox_inches = bbox_inches, dpi = dpi)



def save_pdf(pdf, fig):

    pdf.savefig(fig)