#!/usr/bin/env python
# -*- encoding: utf-8

import unittest

from nltk import NaiveBayesClassifier

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

   def test_classify_emoticons(self):
      self.assertEqual(ec.classify(':)'), (POS, 1.0))

   def test_classify_nonwords(self):
      self.assertEqual(ec.classify('zzzzz'), (NO_CLASS, 1.0))

   def test_classify_terms(self):
      """Test terms"""
      ec._terms_by_root_form = { 'wygrac': ('wygrali', ) }
      ec._allterms = set(['wygrac', 'wygrali'])
      ec._terms_set = ec._allterms
      cls = NaiveBayesClassifier.train([
                                          ({ 'wygrac': True }, POS),
                                          ({ 'wygrac': True }, POS)
                                        ])
      ec.terms_cls = cls
      self.assertEqual(ec.classify('wygrali'), (POS, 1.0))

   def test_classify_bigrams(self):
      ec._terms_by_root_form = { 'wygrac': ('wygrali', ) }
      ec._allterms = set(['wygrac', 'wygrali'])
      ec._bigrams_set = set(['wygrac wszystko'])
      cls = NaiveBayesClassifier.train([
                                          ({ 'wygrac wszystko': True }, POS),
                                          ({ 'wygrac wszystko': True }, POS)
                                        ])
      ec.bigrams_cls = cls
      self.assertEqual(ec.classify('wygrali wszystko'), (POS, 1.0))

   def test_classify_trigrams(self):
      ec._terms_by_root_form = {
                                 'dostac': ('dostalismy', ),
                                 'duza': ('duze', ),
                                 'nagroda': ('nagrody', ),
                               }
      ec._allterms = set(['dostac', 'dostalismy', 'duza', 'duze', 'nagroda', 'nagrody'])
      ec._trigrams_set = set(['dostac duza nagroda'])
      cls = NaiveBayesClassifier.train([
                                          ({ 'dostac duza nagroda': True }, POS),
                                          ({ 'dostac duza nagroda': True }, POS),
                                          ({ 'dostac duza nagroda': True }, POS),
                                          ({ 'dostac duza nagroda': True }, POS),
                                          ({ 'dostac duza nagroda': True }, NEG),
                                          ({ 'dostac duza nagroda': True }, NEG)
                                        ])
      ec.trigrams_cls = cls
      res = ec.classify(u'Dostaliśmy duże nagrody')
      res = (res[0], round(res[1], 1))
      self.assertEqual(res, (POS, 0.6))


if __name__ == '__main__':
   unittest.main()
