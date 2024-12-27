import os
import sys
from helpers import get_doc, save_doc


# function fix_toc adjusts indentation and titles of TOC entries
def fix_toc(filename='example', doc=None):
    print('Refactoring TOC ...')

    # get the source document
    doc, doc_path, return_doc = get_doc(doc, filename)
    
    # get current TOC
    toc = doc.get_toc(False)

    # helpers for individual chapters (use these as examples to generate your own TOC)
    in_abbrevs = False
    in_symbols = False
    abbreviations_chapter_title = 'Abkürzungen'
    symbols_chapter_title = 'Symbole'
    figure_chapter_title = 'Abbildungen und Tabellen'

    # loop all TOC entries
    new_toc = []
    for lvl, title, page, dest in toc:
        # remove helper headings
        if 'Kapitel ' in title or 'Anhang ' in title:
            continue

        # check if we are in the 'symbols' chapter
        if title == abbreviations_chapter_title:
            in_abbrevs = True
        else:
            if title == symbols_chapter_title:
                in_abbrevs = False
                in_symbols = True
            else:
                if title == figure_chapter_title:
                    in_symbols = False
                    in_abbrevs = False

        # calculate heading level from list number
        list_num_str = title.split()[0]
        num_dots = list_num_str.count('.')
        if list_num_str[0].isnumeric():  # normal chapter
            if num_dots > 0 or len(list_num_str) == 1:
                text_lvl = num_dots + 1
            else:
                text_lvl = 1
        else:  # appendix chapter
            if num_dots > 0 or len(list_num_str) == 2:
                text_lvl = num_dots + 2
            else:
                text_lvl = 1

        # override level if we are in the symbols or abbreviations chapter
        if (in_symbols and title != symbols_chapter_title) or (in_abbrevs and title != abbreviations_chapter_title):
            text_lvl = 2

        # remove list number if hidden in text
        if text_lvl >= 4:
            title = title.replace(list_num_str, '')

        new_toc.append([text_lvl, title, page, dest])

    doc.set_toc(new_toc)
    print('TOC successfully created!')

    # return or save
    if return_doc:
        return doc
    else:
        save_doc(doc, os.path.join(doc_path, filename + '_toced' + '.pdf'))


# handle function calls from console
if __name__ == '__main__':
    # handle call arguments
    if len(sys.argv) == 2:
        fix_toc(sys.argv[1])
    else:
        fix_toc()
