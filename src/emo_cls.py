#!/usr/bin/env python
# -*- encoding: utf-8

from __future__ import division

import re
import csv
import nltk
import gzip
import cPickle
import msgpack

from collections import defaultdict

from feature_extraction import FeatureExtraction

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



class _EmoClassifier(FeatureExtraction):

   def _init(self, words_fn=None, bigrams_fn=None, trigrams_fn=None,
                   terms_by_root_form_fn=None,
                   use_emoticons=False):
      if words_fn:
         words = self._csv_to_dict(words_fn)
         self.words_cls = self._train(words)

      if bigrams_fn:
         bigrams = self._csv_to_dict(bigrams_fn)
         self.bigrams_cls = self._train(bigrams)

      if trigrams_fn:
         trigrams = self._csv_to_dict(trigrams_fn)
         self.trigrams_cls = self._train(trigrams)

      if terms_by_root_form_fn:
         w = gzip.open(terms_by_root_form_fn)
         self.terms_by_root_form = msgpack.unpack(w)
         w.close()

         self.allterms = set([])
         for aroot in self.terms_by_root_form:
            self.allterms.add(aroot)
            for aterm in self.terms_by_root_form[aroot]:
               self.allterms.add(aterm)

      if use_emoticons:
         self.emo_re = {}
         for emo, pattern in emoticons.items():
            patterns = [re.escape(i) for i in pattern]
            self.emo_re[emo] = re.compile(u'|'.join(patterns), re.UNICODE)


   def _train(self, data):
      train_set = []
      for emo in data:
         for aterm in data[emo]:
            freq = int(data[emo][aterm])
            feat_freq = [({ aterm: True }, emo) for i in range(freq)]
            train_set.extend(feat_freq)
      cls = nltk.NaiveBayesClassifier.train(train_set)
      return cls


   def _predict(self, sent):
      return { 'terms': self.extract_terms(sent),
               'bigrams': self.extract_bigrams(sent),
               'trigrams': self.extract_trigrams(sent) }


   def _dump_cls(self, cls, fn):
      w = gzip.open(fn, 'wb')
      cPickle.dump(cls, w, -1)
      w.close()


   def _read_csv(self, fn):
      csv_f = gzip.open(fn)
      csv_reader = csv.reader(csv_f)
      data = []
      for arow in csv_reader:
         data.append(arow)
      csv_f.close()
      return data


   def _csv_to_dict(self, fn):
      raw_data = self._read_csv(fn)
      data = defaultdict(lambda: defaultdict(int))
      for aline in raw_data:
         emo, term, freq = aline
         data[emo][term] = freq
      return data



class EmoClassifier(_EmoClassifier):
   def __init__(self, words_fn=None,
                      bigrams_fn=None,
                      trigrams_fn=None,
                      terms_by_root_form_fn=None,
                      use_emoticons=True):
      self.words_cls = None
      self.bigrams_cls = None
      self.trigrams_cls = None

      self.emo_re = None

      self.terms_by_root_form = None
      self.allterms = None

      self._init(words_fn, bigrams_fn, trigrams_fn,
                 terms_by_root_form_fn,
                 use_emoticons)


   def predict(self, sent):
      return self._predict(sent)
