#!/usr/bin/env python
# -*- encoding: utf-8

import gzip
import os.path
import cPickle

from ec_settings import (TERMS_CLS_DIR, BIGRAMS_CLS_DIR, TRIGRAMS_CLS_DIR)


class ClsCache(object):

   def _dump_cls(self, cls, fn):
      """
         Dump the classifier 'cls' to a pickle named 'fn'.
      """
      w = gzip.open(fn, 'wb')
      cPickle.dump(cls, w, 1)
      w.close()

   def _dump_terms_cls(self, fn=TERMS_CLS_DIR):
      self._dump_cls(self.terms_cls, fn)

   def _dump_bigrams_cls(self, fn=BIGRAMS_CLS_DIR):
      self._dump_cls(self.bigrams_cls, fn)

   def _dump_trigrams_cls(self, fn=TRIGRAMS_CLS_DIR):
      self._dump_cls(self.trigrams_cls, fn)


   def _load_cls(self, fn):
      if not os.path.exists(fn):
         return None
      w = gzip.open(fn, 'rb')
      cls = cPickle.load(w)
      w.close()
      return cls

   def _load_terms_cls(self, fn=TERMS_CLS_DIR):
      return self._load_cls(fn)

   def _load_bigrams_cls(self, fn=BIGRAMS_CLS_DIR):
      return self._load_cls(fn)

   def _load_trigrams_cls(self, fn=TRIGRAMS_CLS_DIR):
      return self._load_cls(fn)

