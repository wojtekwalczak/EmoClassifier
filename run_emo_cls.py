#!/usr/bin/env python
# -*- encoding: utf-8

from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(terms_fn='data/corpuses/terms_raw.csv.gz',
                     bigrams_fn='data/corpuses/bigrams_raw.csv.gz',
                     trigrams_fn='data/corpuses/trigrams_raw.csv.gz',
                     terms_by_root_form_fn='data/terms_by_root_form.msg.gz',
                     use_emoticons=True)

   e.terms_cls.show_most_informative_features(10)
   e.bigrams_cls.show_most_informative_features(10)
   e.trigrams_cls.show_most_informative_features(10)

   example_sents = ( (u'Czuję się dziś bardzo dobrze'),
                     (u'To chyba najlepszy kabaret jaki oglądałem'),
                     (u'Niestety, mieliśmy dużego pecha i przegraliśmy'),
                     (u'Zachorowałem i leżę w łóżku') )

   for sent in example_sents:
      res = e.predict(sent)
      print 'Sentence:', sent
      print '  ->', res.get('terms', '')
      print '  ->', res.get('bigrams', '')
      print '  ->', res.get('trigrams', '')
      print '-'*80
