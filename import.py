#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rdflib, urllib

file_in  = "etymwn.tsv"
file_out = "./data/"
file_ns  = rdflib.Namespace("http://example.org/etymwn#")

g = rdflib.Graph(store='Sleepycat', identifier='etymwn')
g.open(file_out, create=True)

print("Precalculate file size...", end="")
with open(file_in) as f:
    file_in_size = 0
    for line in f:
        file_in_size += 1
print(" Done.")

line_cnt = 1
with open(file_in) as f:
    for line in f:
        triplet = line.rstrip().split("\t")

        # Examples: "p_gem: mus" / "eng: day"
        s_word = triplet[0][triplet[0].find(":")+2:]
        s_lang = triplet[0][:triplet[0].find(":")]
        o_word = triplet[2][triplet[2].find(":")+2:]
        o_lang = triplet[2][:triplet[2].find(":")]
        p      = triplet[1][4:]

        # nodes
        rdf_s = urllib.parse.quote_plus(s_lang + "_" + s_word)
        rdf_o = urllib.parse.quote_plus(o_lang + "_" + o_word)
        rdf_s = file_ns[rdf_s]
        rdf_o = file_ns[rdf_o]

        # lables
        g.add(( rdf_s, rdflib.RDFS.label, rdflib.Literal(s_word) ))
        g.add(( rdf_o, rdflib.RDFS.label, rdflib.Literal(o_word) ))
        # languages
        g.add(( rdf_s, file_ns.lang, rdflib.Literal(s_lang) ))
        g.add(( rdf_o, file_ns.lang, rdflib.Literal(o_lang) ))

        # relation types:
        #
        # - direct
        #   * :lat_miser     :etymological_origin_of :eng_miser
        #   * :eng_misdivide :has_derived_form       :eng_misdivided
        #
        # - reversed
        #   * :eng_misdoings :is_derived_from        :eng_misdoing
        #   * :ita_misero    :etymology              :lat_miser
        #   * :eng_relation  :etymologically_related :eng_relate
        #   * :eng_monie     :variant:orthography    :eng_money
        #
        # - unknown
        #   * derived - ?
        #   * etymologically - ?

        if p in ("etymological_origin_of", "has_derived_form"):
            # direct
            g.add((rdf_s, file_ns.origin_of, rdf_o))
        elif p in ("is_derived_from", "etymology", "variant:orthography"):
            # reversed
            g.add((rdf_o, file_ns.origin_of, rdf_s))
        elif p == "etymologically_related":
            # mutual relation, i.e. useless
            # Example:
            # ang:baswian  rel:etymologically_related  ang:basu
            # ang:basu     rel:etymologically_related  ang:baswian
            continue
        else:
            print(f"\n> Unknown predicate '{p}', skip.")
            print(f">> {line}", end="")
            continue

        if line_cnt % 1000 == 0:
            print(f"\rProcessing {line_cnt:,}/{file_in_size:,}...", end="")
        line_cnt += 1
print(f"\n\rProcessing {file_in_size:,}/{file_in_size:,} Done.")

g.close()
