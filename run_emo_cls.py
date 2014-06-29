#!/usr/bin/env python
# -*- encoding: utf-8

from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(terms_fn='data/corpuses/terms_raw.csv.gz',
                     bigrams_fn='data/corpuses/bigrams_raw.csv.gz',
                     trigrams_fn='data/corpuses/trigrams_raw.csv.gz',
                     terms_by_root_form_fn='data/terms_by_root_form.msg.gz',
                     is_use_emoticons=True,
                     is_dump_cls=True,
                     is_load_cached_cls=True)

   e.terms_cls.show_most_informative_features(10)
   e.bigrams_cls.show_most_informative_features(10)
   e.trigrams_cls.show_most_informative_features(10)

   example_sents = ( (u'Było super, nie wyobrażam sobie lepszych wakacji'),
                     (u'To chyba najlepszy kabaret jaki oglądałem'),
                     (u'Wszystkiego najlepszego i wesołych świąt'),
                     (u'Niestety, mieliśmy dużego pecha i przegraliśmy'),
                     (u'Zachorowałem i leżę w łóżku'),
                     (u'To bardzo smutna wiadomość, nie mogę tego zrozumieć'))

   for sent in example_sents:
      print 'Sentence:', sent
      res = e.classify(sent)
      print 'Classified as:', res
