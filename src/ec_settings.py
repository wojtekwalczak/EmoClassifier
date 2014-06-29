#!/usr/bin/env python
# -*- encoding: utf-8

import os.path

# pickled versions of the classifiers produced by go to CLS_DUMP_DIR
CLS_DIR="data/classifiers"

TERMS_CLS_DIR=os.path.join(CLS_DIR, "terms_cls.pickle")
BIGRAMS_CLS_DIR=os.path.join(CLS_DIR, "bigrams_cls.pickle")
TRIGRAMS_CLS_DIR=os.path.join(CLS_DIR, "trigrams_cls.pickle")


