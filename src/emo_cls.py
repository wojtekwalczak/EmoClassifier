#!/usr/bin/env python
# -*- encoding: utf-8

"""
      Classify the emotional affinity of sentences.
"""
from __future__ import division

import re
import csv
import nltk
import gzip
import cPickle
import msgpack
import os.path

from collections import defaultdict

from feature_extraction import FeatureExtraction
from ec_settings import TERMS_CLS_DIR, BIGRAMS_CLS_DIR, TRIGRAMS_CLS_DIR


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


class _ClsCache(object):

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


class _ReadCorpus(object):

   def _csv_to_dict(self, fn):
      """
         Read in the contents of a CSV file and place the contents
         in a dict of dicts.

         The CSV file is supposed to be of a form:

         val_1,val_2,val_3

         where:
          - 'val_1' is a type of emotion ('pos'/'neg')
          - 'val_2' is a term (bigram/trigram etc.)
          - 'val_3' is a frequency of occurence of 'val_2'
            in the context of 'val_1'

         Return a tuple of two values:
          - a dict of dicts: adict[val_1][val_2] = val_3
          - a tuple of all val_2s (ie. terms/bigrams/trigrams)
      """
      terms = set([])
      raw_data = self._read_csv(fn)
      data = defaultdict(lambda: defaultdict(int))
      for aline in raw_data:
         emo, term, freq = aline
         data[emo][term] = freq
         terms.add(term)
      return data, terms


   def _read_csv(self, fn):
      csv_f = gzip.open(fn)
      csv_reader = csv.reader(csv_f)
      data = []
      for arow in csv_reader:
         data.append(arow)
      csv_f.close()
      return data



class _EmoClassifier(FeatureExtraction, _ClsCache, _ReadCorpus):

   def _init(self, terms_fn=None, bigrams_fn=None, trigrams_fn=None,
                   terms_by_root_form_fn=None,
                   is_use_emoticons=False,
                   is_dump_cls=False,
                   is_load_cached_cls=False):

      terms, self._terms_set = self._csv_to_dict(terms_fn)
      bigrams, self._bigrams_set = self._csv_to_dict(bigrams_fn)
      trigrams, self._trigrams_set = self._csv_to_dict(trigrams_fn)

      if is_load_cached_cls:
         self.terms_cls = self._load_terms_cls()
         self.bigrams_cls = self._load_bigrams_cls()
         self.trigrams_cls = self._load_trigrams_cls()

      if terms_fn and not self.terms_cls:
         self.terms_cls = self._train(terms)
         if is_dump_cls:
            self._dump_terms_cls()

      if bigrams_fn and not self.bigrams_cls:
         self.bigrams_cls = self._train(bigrams)
         if is_dump_cls:
            self._dump_bigrams_cls()

      if trigrams_fn and not self.trigrams_cls:
         self.trigrams_cls = self._train(trigrams)
         if is_dump_cls:
            self._dump_trigrams_cls()

      if terms_by_root_form_fn:
         w = gzip.open(terms_by_root_form_fn)
         self._terms_by_root_form = msgpack.unpack(w, encoding='utf-8')
         w.close()

         # create a set of all terms from 'self._terms_by_root_form'
         # in 'self._allterms'; this is a temporary solution of increasing
         # the speed of looking up for terms to stem
         for aroot in self._terms_by_root_form:
            self._allterms.add(aroot)
            for aterm in self._terms_by_root_form[aroot]:
               self._allterms.add(aterm)

      if is_use_emoticons:
         self._emo_re = {}
         for emo, pattern in emoticons.items():
            patterns = [re.escape(i) for i in pattern]
            self._emo_re[emo] = re.compile(u'|'.join(patterns), re.UNICODE)


   def _train(self, data):
      train_set = []
      for emo in data:
         for aterm in data[emo]:
            freq = int(data[emo][aterm])
            feat_freq = [({ aterm: True }, emo) for i in range(freq)]
            train_set.extend(feat_freq)
      cls = nltk.NaiveBayesClassifier.train(train_set)
      return cls


   def _generic_classify(self, sent, cls, extract_func, what):
      if not cls:
         return None

      feats = extract_func(sent)
      if not feats:
         return '---'
      terms_probdist = cls.prob_classify(feats)

      if self._verbose:
         print " - %s: 'pos' probability: %.2f; 'neg' probability: %.2f"\
                 % (what,
                    terms_probdist.prob('pos'),
                    terms_probdist.prob('neg'))

      return terms_probdist.max()


   def _classify_terms(self, sent):
      return self._generic_classify(sent,
                                    self.terms_cls,
                                    self.extract_terms,
                                    'terms')


   def _classify_bigrams(self, sent):
      return self._generic_classify(sent,
                                    self.bigrams_cls,
                                    self.extract_bigrams,
                                    'bigrams')


   def _classify_trigrams(self, sent):
      return self._generic_classify(sent,
                                    self.trigrams_cls,
                                    self.extract_trigrams,
                                    'trigrams')


   def _classify(self, sent):
      return (self._classify_terms(sent),
              self._classify_bigrams(sent),
              self._classify_trigrams(sent))





class EmoClassifier(_EmoClassifier):
   """
      Classify the emotional affinity of sentences.

      __init__() parameters:
       terms_fn (str)              - a file path to the terms corpus
       bigrams_fn (str)            - a file path to the bigrams corpus
       trigrams_fn (str)           - a file path to the trigrams corpus
       terms_by_root_form_fn (str) - a file path to the dictionary of word
                                     forms (root + inflections)
       is_use_emoticons (bool)     - if 'True', uses emoticons to classify
                                     the emotional affinity of sentences
       is_load_cached_cls (bool)   - if 'True', loads classifiers from cache
                                     instead of training them
       is_dump_cls (bool)          - if 'True', dumps trained classifiers
       verbose (bool)              - if 'True', be talkative


      Class attributes:
       terms_cls   - terms classifier
       bigrams_cls - bigrams classifier
       trigrams    - trigrams classifier

      Class methods:
       classify(sent) - classify sentence 'sent'. Return the classification
                        result

   """
   def __init__(self, terms_fn=None,
                      bigrams_fn=None,
                      trigrams_fn=None,
                      terms_by_root_form_fn=None,
                      is_use_emoticons=True,
                      is_load_cached_cls=False,
                      is_dump_cls=False,
                      verbose=True):
      self._terms_set = None
      self._bigrams_set = None
      self._trigrams_set = None

      self.terms_cls = None
      self.bigrams_cls = None
      self.trigrams_cls = None

      self._emo_re = None

      self._terms_by_root_form = None
      self._allterms = set([])

      self._verbose = verbose

      self._init(terms_fn, bigrams_fn, trigrams_fn,
                 terms_by_root_form_fn,
                 is_use_emoticons=is_use_emoticons,
                 is_dump_cls=is_dump_cls,
                 is_load_cached_cls=is_load_cached_cls)


   def classify(self, sent):
      return self._classify(sent)
