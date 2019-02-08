# Offline etymological dictionary

## Introduction

Simple Python application for demonstration of typical processing of RDF data:

* data import
* standard (RDFS) and custom vocabularies
* RDF graph building
* storing data into Berkeley DB (Sleepycat)
* RDF graph querying (SPARQL)

Was created for demonstration of proof concept, but can be used for real inquiry of words' etymology:

```sh
> python ./dictionary.py --lang=eng scholar
```

Result:

```
scholar — English
 < scoler — Middle English (1100-1500)
  < scolere — Old English (ca. 450-1100)
   < scholaris — Latin
    < schola — Latin
     < σχολή — Ancient Greek (to 1453)
      < σχολεῖον — Ancient Greek (to 1453)
```

## Pre-requisites

1. Install Python 3 libraries: `rdflib`, `bsddb`.
1. Download ["Etymological Wordnet 2013-02-08"](http://icsi.berkeley.edu/~demelo/etymwn/) dataset extracted by Gerard de Melo from English Wiktionary (License: CC-BY-SA 3.0). Direct download link:

    [etymwn-20130208.zip](https://cs.rutgers.edu/~gd343/downloads/etymwn-20130208.zip) (26.2 Mb)

1. Extract zip-file into the project folder (`etymological-dictionary/etymwn.tsv`).
1. Run `python ./import.py` to import data into the internal database. It will take about 1 hour of time and 3.8 Gb of space.

## Usage

Run `dictionary.py` with two parameters: a word and the corresponding ISO 639-3 language code:

```sh
> python ./dictionary.py --lang=eng muscular
```

To integrate the etymology dictionary into the GoldenDict application:

1. Open Edit|Dictionaries...
1. On the "Programs" tab add new item:

    * type: Plain text
    * command: python /path/to/dictionary.py --lang=eng %GDWORD%
    
1. Add the newly created source to your dictionary set on the "Groups" tab
