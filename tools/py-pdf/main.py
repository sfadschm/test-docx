import os
import fitz

from toc import fix_toc
from vectorize import vectorize
from helpers import get_doc, save_doc

if __name__ == '__main__':
    # check PyMuPDF version
    if tuple(map(int, fitz.VersionBind.split('.'))) < (1, 19, 5):
        raise ValueError('PyMuPDF v1.19.5+ is required!')

    # get document
    doc, doc_path, _ = get_doc(None, 'example')

    # finalize document
    doc_toced = fix_toc('', doc)
    print()
    doc_veced = vectorize('', doc_toced)
    print()

    # save document
    save_doc(doc_veced, os.path.join(doc_path, 'example' + '_finalized' + '.pdf'))
