#!/usr/bin/env python
# -*- encoding: utf-8

"""
      Classify the emotional affinity of sentences.
"""
from __future__ import division

import re
import gzip
import codecs
import msgpack

import nltk

from feature_extraction import FeatureExtraction, emoticons
from cls_cache import ClsCache
from corpus_reader import CorpusReader
from ec_settings import (POS, NEG, NO_CLASS,
                         TERMS_FN, BIGRAMS_FN, TRIGRAMS_FN,
                         TERMS_BY_ROOT_FORM_FN)


DictionaryProbDist = nltk.probability.DictionaryProbDist


class _EmoClassifier(FeatureExtraction, ClsCache, CorpusReader):

   def _init(self, terms_fn=None, bigrams_fn=None, trigrams_fn=None,
                   terms_by_root_form_fn=None,
                   is_use_emoticons=False,
                   is_dump_cls=False,
                   is_load_cached_cls=False):

      # load dictionaries of terms/bigrams/trigrams (first element)
      # and sets of all terms/bigrams/trigrams
      if terms_fn:
         terms, self._terms_set = self._csv_to_dict(terms_fn)

      if bigrams_fn:
         bigrams, self._bigrams_set = self._csv_to_dict(bigrams_fn)

      if trigrams_fn:
         trigrams, self._trigrams_set = self._csv_to_dict(trigrams_fn)

      # try to load cached classifiers
      if is_load_cached_cls:
         self.terms_cls = self._load_terms_cls()
         self.bigrams_cls = self._load_bigrams_cls()
         self.trigrams_cls = self._load_trigrams_cls()

      # train classifiers if it didn't work
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

      # load dictinary for stemming purposes
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


   def _train(self, data):
      train_set = []
      for emo in data:
         for aterm in data[emo]:
            freq = int(data[emo][aterm])
            feat_freq = [({ aterm: True }, emo) for i in range(freq)]
            train_set.extend(feat_freq)
      cls = nltk.NaiveBayesClassifier.train(train_set)
      return cls


   def _classify_emoticons(self, sent):
      pos = self.extract_emoticons(sent, POS)
      neg = self.extract_emoticons(sent, NEG)
      lpos, lneg = len(pos), len(neg)

      # no emoticons found
      if lpos+lneg == 0:
         return DictionaryProbDist({ POS: 0, NEG: 0 })

      # ensure no ZeroDivisionError exceptions will happen
      pos_prob = 1.0 if lneg==0 else lpos / (lpos+lneg)

      terms_probdist = DictionaryProbDist({ POS: pos_prob,
                                            NEG: 1 - pos_prob })

      if self._verbose:
         print " - %s: '%s' probability: %.2f; '%s' probability: %.2f"\
                 % ('emoticons',
                    POS, terms_probdist.prob(POS),
                    NEG, terms_probdist.prob(NEG))

      return terms_probdist



   def _generic_classify(self, sent, cls, extract_func, what):
      if not cls:
         return None

      feats = extract_func(sent)
      if not feats:
         return DictionaryProbDist({ POS: 0, NEG: 0 })
      terms_probdist = cls.prob_classify(feats)

      if self._verbose:
         print " - %s: '%s' probability: %.2f; '%s' probability: %.2f"\
                 % (what,
                    POS, terms_probdist.prob(POS),
                    NEG, terms_probdist.prob(NEG))

      return terms_probdist


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
      res = (self._classify_terms(sent),
             self._classify_bigrams(sent),
             self._classify_trigrams(sent),
             self._classify_emoticons(sent))

      # only NO_CLASS in res
      if res.count(NO_CLASS) == len(res):
         return NO_CLASS, 1.0

      # count mean pos/neg probability
      neg, pos, counter = 0, 0, 0
      for score in res:
         if score is None: # no such classifier
            continue

         cur_pos, cur_neg = score.prob(POS), score.prob(NEG)

         if cur_pos + cur_neg == 0: # no features provided
            continue

         pos += cur_pos
         neg += cur_neg
         counter += 1

      if counter == 0:
         return NO_CLASS, 1.0

      pos = pos / counter
      neg = neg / counter

      if pos > neg:
         return POS, pos
      elif neg > pos:
         return NEG, neg
      return NO_CLASS, 1.0




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
       test_set    - a list of tuples containing sentences and labels


      Class methods:
       classify(sent)     - classify sentence 'sent'. Return the classification
                            result
       accuracy(test_set) - return accuracy measure for test_set (if not set,
                            check self.test_set)
       print_confusion_matrix(gold, test) - given two lists of labels (gold
                                            and test) return confusion matrix
       load_test_set(fn) - load test set from file 'fn'

   """
   def __init__(self, terms_fn=TERMS_FN,
                      bigrams_fn=BIGRAMS_FN,
                      trigrams_fn=TRIGRAMS_FN,
                      terms_by_root_form_fn=TERMS_BY_ROOT_FORM_FN,
                      is_use_emoticons=True,
                      is_load_cached_cls=False,
                      is_dump_cls=False,
                      verbose=False):
      self._terms_set = None
      self._bigrams_set = None
      self._trigrams_set = None

      self.terms_cls = None
      self.bigrams_cls = None
      self.trigrams_cls = None

      self.test_set = None

      self._emo_re = None

      self._terms_by_root_form = None
      self._allterms = set([])

      self._verbose = verbose

      self._init(terms_fn, bigrams_fn, trigrams_fn,
                 terms_by_root_form_fn,
                 is_use_emoticons=is_use_emoticons,
                 is_dump_cls=is_dump_cls,
                 is_load_cached_cls=is_load_cached_cls)


   @property
   def test_set_labels(self):
      if not self.test_set:
         return []
      return [i[1] for i in self.test_set]


   @property
   def test_set_sents(self):
      if not self.test_set:
         return []
      return [i[0] for i in self.test_set]


   def load_testset(self, fn):
      """
         Load testset from file 'fn'.

         The file format is:
         label:sentence\n
         ...

         Returns a generator of tuples: (sentence1, label1), ...
      """
      w = codecs.open(fn, 'r', 'utf-8')
      data = w.read().split('\n')[:-1]
      w.close()

      # split labels and sentences
      data = [i.split(':') for i in data]
      # reverse elements and connect subsentences in case of additional colons
      self.test_set = [(':'.join(z[1:]), z[0]) for z in data]
      return self.test_set


   def accuracy(self, test_set=None):
      test_set = test_set if test_set else self.test_set
      if not test_set:
         raise Exception("No test set provided!")
      return nltk.classify.accuracy(self, test_set)


   def print_confusion_matrix(self, gold, test):
      cm = nltk.ConfusionMatrix(gold, test)
      print cm.pp()


   def classify(self, sent):
      return self._classify(sent)


   def batch_classify(self, sents):
      """NLTK-2.0 compatibility"""
      self.classify_many(sent)


   def classify_many(self, sents):
      for sent in sents:
         yield self._classify(sent)[0]
