#!/usr/bin/env python
# -*- encoding: utf-8

import unittest
from src.feature_extraction import FeatureExtraction

fe = FeatureExtraction()

class TestFeatureExtraction(unittest.TestCase):

   def test_normalize_sentence(self):
      self.assertEqual(fe._normalize_sentence(u'Łódź'), u'lodz')


   def test_extract_words(self):
      self.assertEqual(fe._extract_words('I123want to pass $ this test!!!'),
                                 ['I', 'want', 'to', 'pass', 'this', 'test'])


   def test_reduce_extended_chars(self):
      self.assertEqual(fe._reduce_extended_chars('Hurraaaaa wygraaaaliiii'),
                                                             'Hurra wygrali')

   def test_stem_term(self):
      fe._terms_by_root_form = { 'wygrac': ('wygrali', ) }
      fe._allterms = set(['wygrac', 'wygrali'])
      self.assertEqual(fe._stem_term('wygrali'), 'wygrac')


   def test_stem_term_2(self):
      self.assertEqual(fe._stem_term('no_dictionary'), 'no_dictionary')


   def test_stem_sentence(self):
      fe._terms_by_root_form = {
                                 'miec': ('mielismy', ),
                                 'pech': ('pecha', ),
                                 'przegrac': ('przegralismy', ),
                               }

      fe._allterms = set([i[0] for i in fe._terms_by_root_form.values()])
      self.assertEqual(fe._stem_sentence('mielismy pecha, ze przegralismy'),
                                                    'miec pech, ze przegrac')


   def test_extract_emoticons_pos(self):
      self.assertEqual(fe.extract_emoticons('$$$$:)1111:(xx:Dxx', 'pos'),
                                            [':)', ':D'])

   def test_extract_emoticons_neg(self):
      self.assertEqual(fe.extract_emoticons('>.<**):@1111:(xx:Dxx:)', 'neg'),
                                            ['>.<', ':@', ':('])



if __name__ == '__main__':
   unittest.main()
