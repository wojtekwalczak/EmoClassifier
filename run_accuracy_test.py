#!/usr/bin/env python
# -*- encoding: utf-8

from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(is_load_cached_cls=True)

   e.load_testset('data/testsets/test1.txt')
   print e.accuracy()
