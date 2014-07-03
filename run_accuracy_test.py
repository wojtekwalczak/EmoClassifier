#!/usr/bin/env python
# -*- encoding: utf-8

from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(is_load_cached_cls=True)
   e.load_testset('data/testsets/test1.txt')

   print 'Accuracy: %s\n' % (e.accuracy())

   # confusion matrix
   test_labels = [e.classify(sent)[0] for sent in e.test_set_sents]
   print 'Confusion matrix:'
   e.print_confusion_matrix(e.test_set_labels, test_labels)
