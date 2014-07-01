#!/usr/bin/env python
# -*- encoding: utf-8

import unittest
from src.emo_cls import EmoClassifier
from src.ec_settings import POS, NEG, NO_CLASS

ec = EmoClassifier(terms_fn=None,
                   bigrams_fn=None,
                   trigrams_fn=None,
                   terms_by_root_form_fn=None,
                   verbose=False,
                   is_dump_cls=False,
                   is_load_cached_cls=False)

class TestEmoClassifier(unittest.TestCase):

   def test_classify_v1(self):
      self.assertEqual(ec.classify(':)'), (POS, 1.0))

   def test_classify_v2(self):
      self.assertEqual(ec.classify('zzzzz'), (NO_CLASS, 1.0))


if __name__ == '__main__':
   unittest.main()
