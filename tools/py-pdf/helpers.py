import os
import fitz


def get_doc(doc, filename):
    # get the source document
    cwd = os.getcwd()
    thesis_dir = os.path.join(os.path.dirname(os.path.dirname(cwd)), 'document', 'releases')
    src_path = os.path.join(thesis_dir, filename + '.pdf')

    # early exit if doc already provided
    return_doc = False
    if doc is None:
        doc = fitz.open(src_path)
    else:
        return_doc = True

    return doc, thesis_dir, return_doc


def save_doc(doc, save_path):
    print('Saving document ...')
    doc.save(save_path, deflate=True, use_objstms=1, garbage=4)
    print('Thesis successfully saved!')
