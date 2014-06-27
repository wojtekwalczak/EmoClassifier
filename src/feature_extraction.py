#!/usr/bin/env python
# -*- encoding: utf-8

import re

from unicodedata import normalize, combining

from nltk.collocations import (BigramAssocMeasures,
                               TrigramAssocMeasures,
                               BigramCollocationFinder,
                               TrigramCollocationFinder)



class _FeatureExtraction(object):

   def _preprocess_sent(self, sent, return_list=False):
      sent = self._normalize_sentence(sent)
      sent = self._reduce_extended_chars(sent)
      sent = self._stem_sentence(sent)
      if return_list:
         return self._extract_words(sent)
      return { i: True for i in self._extract_words(sent) }


   def _extract_words(self, sent):
      return re.findall(r"[^\W\d_ ]+", sent)


   def _normalize_sentence(self, sent):
      """
         Replace diacritics with regular characters.
      """
      sent = sent.lower().replace(u'ł', u'l')
      t1 = None
      try:
         t1 = normalize('NFD', sent)
      except UnicodeDecodeError:
         t1 = normalize('NFD', sent.decode('utf-8'))
      return ''.join(c for c in t1 if not combining(c))


   def _stem_term(self, term_raw):
      aterm = term_raw.lower().strip()
      if len(aterm) < 3:
         return aterm
      if aterm in self.terms_by_root_form:
         return aterm
      if not aterm in self.allterms:
         return aterm
      for aroot in self.terms_by_root_form:
         if aterm in [i.decode('utf-8') for i in self.terms_by_root_form[aroot]]:
            return aroot
      return aterm


   def _stem_sentence(self, sent):
      stemmed_sent = sent[:]
      for aword_raw in re.findall(r"[^\W\d_ ]+", sent):
         stemmed = self._stem_term(aword_raw)
         if stemmed != aword_raw:
            stemmed_sent = re.sub(aword_raw, stemmed, sent)
      return stemmed_sent


   def _reduce_extended_chars(self, sent):
      return re.sub(r"(.)\1{2,100}", r"\1", sent)


class FeatureExtraction(_FeatureExtraction):

   def extract_emoticons(self, sent):
      pass


   def extract_terms(self, sent):
      return self._preprocess_sent(sent)


   def extract_bigrams(self, sent):
      sent = self._preprocess_sent(sent, return_list=True)
      bigram_measures = BigramAssocMeasures()
      BiFinder = BigramCollocationFinder.from_words(sent)
      bigrams = BiFinder.nbest(bigram_measures.pmi, 10000)
      return { ' '.join(i): True for i in bigrams }


   def extract_trigrams(self, sent):
      sent = self._preprocess_sent(sent, return_list=True)
      trigram_measures = TrigramAssocMeasures()
      TriFinder = TrigramCollocationFinder.from_words(sent)
      trigrams = TriFinder.nbest(trigram_measures.pmi, 10000)
      return { ' '.join(i): True for i in trigrams }

