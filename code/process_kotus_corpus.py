#!/usr/bin/env python
# coding: utf-8

"""Find morphological patterns between nouns and 
verbs in the Finnish language via Kotus' XML corpus 
(cf. kaino.kotus.fi/sanat/nykysuomi), log them in TXTs 
and clean the original corpus from such derivations 
leaving only the nouns that cannot be derived into verbs, 
and vice versa, i.e. sterile lexical units for further 
analysis as for why they are morphologically unaccessible
in an agglutinative language like Finnish.
"""

import os

from lxml import etree


def clean_non_noun_verb_categories(tree: etree._ElementTree):
    """Clean the Kotus corpus from irrelevant lexical categories,
    i.e. adjectives (14, 15, 16, 17, 26, 34, 35, 36, 37, 41, 42, 47),
    loanwords (32), numerals (31, 45, 46), adverbs (99), etc. 
    (cf. sanalistan-kuvaus.txt)

    Args:
        tree (etree._ElementTree): tree of the Kotus' XML document.
    """
    other_encodings = [
    14, 15, 16, 17, 26, 31, 32, 34, 
    35, 36, 37, 43, 45, 46, 99
    ]
    with open('kotus-sanalista_cleaned.xml', 'a', encoding="utf-8") as xml:
        xml.write("<?xml version='1.0' encoding='utf-8'?>\n<kotus-sanalista>\n")
        for elem in tree.xpath("/kotus-sanalista/st/t/tn"):
            if int(elem.text) not in other_encodings:
                xml.write(etree.tostring(elem.getparent().getparent(), encoding=str))
        xml.write("</kotus-sanalista>\n")
    xml.close()


def find_noun_2_verb_relations(path: str):
    """Find N↔V derivations by comparing strings 
    from 12 to 5 and eliminating the patterns after each 
    pass, with results written in the reference TXTs.

    Args:
        path (str): path to XML.
    """
    shortened_path = path.rsplit('/', 1)[0]
    os.chdir(shortened_path)
    clean_non_noun_verb_categories(etree.parse(path.split('/')[-1]))
    tree = etree.parse("kotus-sanalista_cleaned.xml")
    root = tree.getroot()
    noun_encodings = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 18, 
    19, 20, 21, 22, 23, 24, 25, 27, 28, 29, 30, 33, 
    38, 39, 40, 41, 42, 44, 47, 48, 49, 50, 51
    ]
    for i in list(range(0, 8)):
        threshold =  12 - i
        print(f'Comparing {threshold} first characters of each N and V')
        current_file = f'{shortened_path}/output-{threshold}.txt'
        with open(current_file, 'a', encoding="utf-8") as output:
            _temp_noun_list_ = []
            _temp_verb_list_ = []
            output.write(f"N→V derivations by {threshold} common characters:\n")
            for elem in tree.xpath("/kotus-sanalista/st/t/tn"):
                if int(elem.text) in noun_encodings:
                    _temp_noun_list_.append(
                        elem.getparent().getparent().getchildren()[0].text
                    )
                if int(elem.text)>=52 and int(elem.text)<=78:  # Verb encodings 
                    _temp_verb_list_.append(
                        elem.getparent().getparent().getchildren()[0].text
                    )
            for noun in _temp_noun_list_:
                temp_var = False
                is_verified = False
                for verb in _temp_verb_list_:
                    if noun[:threshold]==verb[:threshold] and is_verified==False:
                        temp_var = True
                        is_verified = True
                        output.write(f"{noun} → {verb}\n")
                        for entry in tree.xpath('/kotus-sanalista/st/s'):
                            text_entry = entry.text
                            if text_entry==noun or text_entry==verb:
                                root.remove(entry.getparent())
            with open('kotus-sanalista_cleaned.xml', 'wb') as xml:
                tree.write(xml, encoding='utf-8')
                xml.close()
    output.close()
    print('Done')


if __name__ == "__main__":
    FILEPATH = 'C:/your-path/kotus-sanalista_v1.xml'
    find_noun_2_verb_relations(FILEPATH)
