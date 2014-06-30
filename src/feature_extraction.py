#!/usr/bin/env python
# -*- encoding: utf-8

"""
   Extract features from a sentence.
"""

import re
from unicodedata import normalize, combining

from nltk.collocations import (BigramAssocMeasures,
                               TrigramAssocMeasures,
                               BigramCollocationFinder,
                               TrigramCollocationFinder)

emoticons = {
   'pos':  [u':-)', u':)',  u':o)', u':]', u':3', u':c)',
            u':>',  u'=]',  u'8)',  u'=)', u':}', u':^)', u':っ)',
            u':-D', u':D',  u'8-D', u'8D', u'x-D', u'xD', u'X-D',
            u'XD',  u'=-D', u'=D',  u'=-3', u'=3', u'B^D',
            u":'-)", u":')", # tears of happiness
            u'<3',
            u';-)', u';)', u'*-)', u'*)', u';-]', u';]', # wink
            u';D', u';^)', u':-,',
           ],

   'neg': [u'>:[', u':-(', u':(', u':-c', u':c', u':-<', u':っC',
           u':<',  u':-[', u':[', u':{',
           u":'-(", u":'(", # crying
           u':-|', u':@', u'>:(', # angry
           u'>:\\', u'>:/', u':-/', u':-.', u':/', u':\\', # skeptical
           u'=/', u'=\\',
           u':L', u'=L', u':S', u'>.<',
          ],

}


emo_re = {}
for emo, pattern in emoticons.items():
   patterns = [re.escape(i) for i in pattern]
   emo_re[emo] = re.compile(u'|'.join(patterns), re.UNICODE)


class _FeatureExtraction(object):

   def _preprocess_sent(self, sent):
      sent = sent.lower().strip()
      sent = self._normalize_sentence(sent)
      sent = self._reduce_extended_chars(sent)
      sent = self._stem_sentence(sent)
      return self._extract_words(sent)


   def _extract_words(self, sent):
      """
         Extract strings from 'sent'. Return a list.

         For example:
          >>> re.findall(r"[^\W\d_ ]+", "This123is a sentence :-)")
          ['This', 'is', 'a', 'sentence']
      """
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
      if aterm in self._terms_by_root_form:
         return aterm
      if not aterm in self._allterms:
         return aterm
      for aroot in self._terms_by_root_form:
         if aterm in self._terms_by_root_form[aroot]:
            return aroot
      return aterm


   def _stem_sentence(self, sent):
      stemmed_sent = sent[:]
      for aword_raw in self._extract_words(sent):
         stemmed = self._stem_term(aword_raw)
         if stemmed != aword_raw:
            stemmed_sent = re.sub(aword_raw, stemmed, stemmed_sent)
      return stemmed_sent


   def _reduce_extended_chars(self, sent):
      """
         Reduce "extended" characters in a sentence. "Extended" means
         three or more consecutive occurrences of the same character
         in a word.

         Return the reduced string.

         For example:

         >>> re.sub(r"(.)\1{2,100}", r"\1", "Hurrrrra wygraaaaaliiiii")
         'Hura wygrali'

         This solution is not perfect as it (on purpose) doesn't
         reduce two identical consecutive chars to a single char:

         >>> re.sub(r"(.)\1{2,100}", r"\1", "Hurra wygraaaaaliiiii")
         'Hurra wygrali'
      """
      return re.sub(r"(.)\1{2,100}", r"\1", sent)


class FeatureExtraction(_FeatureExtraction):

   def extract_emoticons(self, sent, atype):
      return re.findall(emo_re[atype], sent)


   def extract_terms(self, sent):
      terms = set(self._preprocess_sent(sent))
      terms = terms & self._terms_set
      return { i: True for i in terms }


   def extract_bigrams(self, sent):
      sent = self._preprocess_sent(sent)
      bigram_measures = BigramAssocMeasures()
      BiFinder = BigramCollocationFinder.from_words(sent)
      bigrams = BiFinder.nbest(bigram_measures.pmi, 10000)
      bigrams = set([' '.join(i) for i in bigrams])
      bigrams = bigrams & self._bigrams_set
      return { i: True for i in bigrams }


   def extract_trigrams(self, sent):
      sent = self._preprocess_sent(sent)
      trigram_measures = TrigramAssocMeasures()
      TriFinder = TrigramCollocationFinder.from_words(sent)
      trigrams = TriFinder.nbest(trigram_measures.pmi, 10000)
      trigrams = set([' '.join(i) for i in trigrams])
      trigrams = trigrams & self._trigrams_set
      return { i: True for i in trigrams }

