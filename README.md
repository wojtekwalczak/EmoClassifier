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
   print```

Output:

```
Sentence: Było super, nie wyobrażam sobie lepszych wakacji
 - terms: 'pos' probability: 0.60; 'neg' probability: 0.40
 - bigrams: 'pos' probability: 0.65; 'neg' probability: 0.35
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65

Sentence: To chyba najlepszy kabaret jaki oglądałem
 - terms: 'pos' probability: 0.91; 'neg' probability: 0.09
 - bigrams: 'pos' probability: 0.39; 'neg' probability: 0.61
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65

Sentence: Wszystkiego najlepszego i wesołych świąt
 - terms: 'pos' probability: 0.99; 'neg' probability: 0.01
 - bigrams: 'pos' probability: 0.94; 'neg' probability: 0.06
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65

Sentence: Niestety, mieliśmy dużego pecha i przegraliśmy
 - terms: 'pos' probability: 0.06; 'neg' probability: 0.94
 - bigrams: 'pos' probability: 0.39; 'neg' probability: 0.61
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65

Sentence: Zachorowałem i leżę w łóżku
 - terms: 'pos' probability: 0.05; 'neg' probability: 0.95
 - bigrams: 'pos' probability: 0.39; 'neg' probability: 0.61
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65

Sentence: To bardzo smutna wiadomość, nie mogę tego zrozumieć
 - terms: 'pos' probability: 0.03; 'neg' probability: 0.97
 - bigrams: 'pos' probability: 0.00; 'neg' probability: 1.00
 - trigrams: 'pos' probability: 0.35; 'neg' probability: 0.65```
