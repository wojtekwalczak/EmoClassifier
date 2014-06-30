#!/usr/bin/env python
# -*- encoding: utf-8

import os.path

NO_CLASS = '---'

# pickled versions of the classifiers produced by go to CLS_DUMP_DIR
CLS_DIR = "data/classifiers"

TERMS_CLS_DIR    = os.path.join(CLS_DIR, "terms_cls.pickle")
BIGRAMS_CLS_DIR  = os.path.join(CLS_DIR, "bigrams_cls.pickle")
TRIGRAMS_CLS_DIR = os.path.join(CLS_DIR, "trigrams_cls.pickle")

TERMS_FN              = 'data/corpuses/terms_raw.csv.gz'
BIGRAMS_FN            = 'data/corpuses/bigrams_raw.csv.gz'
TRIGRAMS_FN           = 'data/corpuses/trigrams_raw.csv.gz'
TERMS_BY_ROOT_FORM_FN = 'data/terms_by_root_form.msg.gz'

