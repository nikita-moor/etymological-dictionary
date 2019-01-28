#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rdflib
import urllib
import rdflib.plugins.sparql as sparql
import csv
import sys, os
import argparse

file_in = "data/"
data_ns = rdflib.Namespace("http://example.org/etymwn#")

def main(argv):
    # --- init -----------------------------------------------------------------
    work_dir = os.path.dirname(os.path.realpath(__file__))

    # --- read arg -------------------------------------------------------------
    parser = argparse.ArgumentParser(description="Etimology dictionary (based on Wiktionary)")
    parser.add_argument("text", type=str, nargs="*",
                        help="a word to look for in the dictionary")
    parser.add_argument("--lang", type=str, default="eng",
                        help="language code from ISO 639-3 (default: %(default)s)")
    args = parser.parse_args()
    in_word = " ".join(args.text).lower()
    in_lang = args.lang

    if len(in_word) == 0:
        parser.print_help()
        sys.exit(2)

    # --- language codes (ISO 639-3) -------------------------------------------
    iso_lang = {}
    with open("iso-639-3.tab", newline="") as f:
        reader = csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        for row in reader:
            iso_lang[row[0]] = row[1]

    # --- query RDF graph for the word's etymology -----------------------------
    g = rdflib.Graph(store='Sleepycat', identifier='etymwn')
    g.open(work_dir + "/" + file_in, create=False)

    w_start = urllib.parse.quote_plus(in_lang + "_" + in_word)
    w_start = data_ns[w_start]
    if (w_start, None, None) not in g:
        print(f"Cannot find '{in_lang}:{in_word}' in the database!")
        sys.exit(0)

    q = sparql.prepareQuery(
        """SELECT DISTINCT ?w_lang ?w_label
           WHERE {
             ?w etymwn:origin_of+ ?w_start ;
                rdfs:label  ?w_label ;
                etymwn:lang ?w_lang .
           }
           LIMIT 10
        """,
        initNs={'etymwn': data_ns, 'rdfs': rdflib.RDFS}
    )
    qres = g.query(q, initBindings={'w_start': w_start})
    if len(qres) == 0:
        print("No ancestors.")
        sys.exit(2)

    # --- print result ---------------------------------------------------------
    print(f"\u202A{in_word} — {iso_lang.get(in_lang, in_lang)}")
    indent = ""
    for row in qres:
        indent += " "
        lang = iso_lang.get(str(row[0]), str(row[0]))
        word = row[1]
        print(f"\u202A{indent}< {word} — {lang}")

    g.close()


if __name__ == "__main__":
    main(sys.argv[1:])
