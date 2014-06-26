#!/usr/bin/env python
# -*- encoding: utf-8

from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(words_fn='data/corpuses/words_raw.csv.gz',
                     bigrams_fn='data/corpuses/bigrams_raw.csv.gz',
                     trigrams_fn='data/corpuses/trigrams_raw.csv.gz',
                     terms_by_root_form_fn='data/terms_by_root_term.msg.gz',
                     use_emoticons=True)

   e.words_cls.show_most_informative_features(10)
   e.bigrams_cls.show_most_informative_features(10)
   e.trigrams_cls.show_most_informative_features(10)

