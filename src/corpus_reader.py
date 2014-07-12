#!/usr/bin/env python
# -*- encoding: utf-8

import csv
import gzip

from collections import defaultdict
from ec_settings import POS, NEG


class CorpusReader(object):

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
         term, pos_freq, neg_freq = aline
         data[POS][term] = pos_freq
         data[NEG][term] = neg_freq
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
