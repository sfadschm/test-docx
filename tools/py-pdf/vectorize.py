import sys
import os
import re
from glob import glob
import fitz

from helpers import get_doc, save_doc


# function vectorize replaces all bitmaps with indexed vector images
def vectorize(filename='example', doc=None):
    print('Vectorizing ...')

    # get the source document
    doc, doc_path, return_doc = get_doc(doc, filename)
    
    # get source directory for images
    cwd = os.getcwd()
    img_dir = os.path.join(os.path.dirname(os.path.dirname(cwd)), 'document', 'images')

    # get vector image list
    vectors = find_ext(img_dir, 'pdf')
    num_vectors = len(vectors)

    # sort vector images naturally
    vectors = sort_natural(vectors)

    # loop through pages
    img_counter = 0
    for page in doc:
        # get images on current page
        img_list = page.get_images(True)

        # loop images on current page
        for img in img_list:
            # get image reference
            bitmap_x_ref = img[0]

            # get the bbox of the bitmap
            bbox = page.get_image_bbox(img)
            bx = (bbox.x0 + bbox.x1)/2
            by = (bbox.y0 + bbox.y1)/2

            # remove the bitmap from the page
            page.delete_image(bitmap_x_ref)

            # insert vector image into bbox
            if img_counter < num_vectors:
                print('Replacing ' + vectors[img_counter].replace(img_dir, '') + ' (p. ' + str(page.number + 1) + ') '
                                                                                                                  '...')

                # open vector image
                src = fitz.open(vectors[img_counter])

                # read dimensions
                vbox = src[0].mediabox
                v_width = vbox.x1 - vbox.x0
                v_height = vbox.y1 - vbox.y0

                # transform the bbox to fit the vector image dimensions
                nbox = fitz.Rect(bx - v_width / 2, by - v_height / 2, bx + v_width / 2, by + v_height / 2)

                # insert vector image
                page.show_pdf_page(nbox, src, 0)

            # increase image counter
            img_counter = img_counter + 1

    # check number of images
    if img_counter != num_vectors:
        raise ValueError('Number of vector images (' + format(num_vectors) +
                         ') not equal to number of bitmaps in source file (' + format(img_counter) + ')!')
    else:
        print('Document successfully vectorized!')

        # return or save
        if return_doc:
            return doc
        else:
            save_doc(doc, os.path.join(doc_path, filename + '_vectorized' + '.pdf'))


# function find_ext finds all files with the given extension in the given folder
def find_ext(dr, ext):
    # ref.: https://stackoverflow.com/a/33998948
    return glob(os.path.join(dr, '*.{}'.format(ext)))


# sort a string list alphanumerically (natural sort)
def sort_natural(unsorted_list):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(unsorted_list, key=alphanum_key)


# handle function calls from console
if __name__ == '__main__':
    # check PyMuPDF version
    if tuple(map(int, fitz.VersionBind.split('.'))) < (1, 19, 5):
        raise ValueError('PyMuPDF v1.19.5+ is required!')

    # handle call arguments
    if len(sys.argv) == 2:
        vectorize(sys.argv[1])
    else:
        vectorize()
