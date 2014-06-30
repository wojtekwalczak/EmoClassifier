EmoClassifier
=============

**Classifies the emotional affinity of sentences in Polish**

WARNING: work in progress :-)

Example usage:

```python
from src.emo_cls import EmoClassifier

e = EmoClassifier(terms_fn='data/corpuses/terms_raw.csv.gz',
                  bigrams_fn='data/corpuses/bigrams_raw.csv.gz',
                  trigrams_fn='data/corpuses/trigrams_raw.csv.gz',
                  terms_by_root_form_fn='data/terms_by_root_form.msg.gz')

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
   print
```

Output:

```
Sentence: Było super, nie wyobrażam sobie lepszych wakacji
 - terms: 'pos' probability: 0.77; 'neg' probability: 0.23
 - bigrams: 'pos' probability: 0.56; 'neg' probability: 0.44
 - trigrams: 'pos' probability: 0.39; 'neg' probability: 0.61
Classified as: ('pos', 'pos', 'neg')

Sentence: To chyba najlepszy kabaret jaki oglądałem
 - terms: 'pos' probability: 0.90; 'neg' probability: 0.10
 - bigrams: 'pos' probability: 0.39; 'neg' probability: 0.61
Classified as: ('pos', 'neg', '---')

Sentence: Wszystkiego najlepszego i wesołych świąt
 - terms: 'pos' probability: 1.00; 'neg' probability: 0.00
 - bigrams: 'pos' probability: 1.00; 'neg' probability: 0.00
Classified as: ('pos', 'pos', '---')

Sentence: Niestety, mieliśmy dużego pecha i przegraliśmy
 - terms: 'pos' probability: 0.04; 'neg' probability: 0.96
Classified as: ('neg', '---', '---')

Sentence: Zachorowałem i leżę w łóżku
 - terms: 'pos' probability: 0.12; 'neg' probability: 0.88
Classified as: ('neg', '---', '---')

Sentence: To bardzo smutna wiadomość, nie mogę tego zrozumieć
 - terms: 'pos' probability: 0.04; 'neg' probability: 0.96
 - bigrams: 'pos' probability: 0.00; 'neg' probability: 1.00
 - trigrams: 'pos' probability: 0.06; 'neg' probability: 0.94
Classified as: ('neg', 'neg', 'neg')
```
