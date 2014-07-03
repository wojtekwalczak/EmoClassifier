EmoClassifier
=============

**Classifies the emotional affinity of sentences in Polish**

WARNING: work in progress :-)

The EmoClassifier classifies emotional affinity of sentences based on occurrences of particular terms (i.e. normalized words), bigrams, trigrams and emoticons.

The classification process may result in providing one of three labels:
 - *pos* for positive affinity
 - *neg* for negative affinity
 - *---* for undefined affinity
The *---* label applies only when none of words/emoticons provided in a sentence is recognized by EmoClassifier.

Currently, the corpuses of terms, bigrams and trigrams come from status updates and comments of Facebook users. First, the positive and negative emoticons were defined. Then Facebook status updates and comments containing any of these emoticons were collected (in sum: 250k of positive messages and 250k of negative messages). Based on these messages, the corpuses of terms, bigrams and trigrams were created.

## Classification

```python
from src.emo_cls import EmoClassifier

e = EmoClassifier(is_dump_cls=True, is_load_cached_cls=True, verbose=True)

example_sents = ( (u'Było super, to były moje najfajniejsze wakacje'),
                  (u'To chyba najzabawniejszy kabaret jaki oglądałem'),
                  (u'Wszystkiego najlepszego i wesołych świąt'),
                  (u'Niestety, mieliśmy dużego pecha i przegraliśmy'),
                  (u'Zachorowałem i leżę w łóżku'),
                  (u'To bardzo smutna wiadomość, nie mogę tego zrozumieć'),
                  (u'Zxcjhgoiu ooijasddnakjz zczxnzbxcz qdqdqqfefw sdsdfsdfsdf'),
                  (u'Przystojniaczek! :-) :D :('))


for sent in example_sents:
   print 'Sentence:', sent
   res = e.classify(sent)
   print 'Classified as: %s (%.2f)\n' % res
```

Output:

```
Sentence: Było super, to były moje najfajniejsze wakacje
 - terms: 'pos' probability: 0.87; 'neg' probability: 0.13
Classified as: pos (0.87)

Sentence: To chyba najzabawniejszy kabaret jaki oglądałem
 - terms: 'pos' probability: 0.54; 'neg' probability: 0.46
Classified as: pos (0.54)

Sentence: Wszystkiego najlepszego i wesołych świąt
 - terms: 'pos' probability: 0.99; 'neg' probability: 0.01
 - bigrams: 'pos' probability: 1.00; 'neg' probability: 0.00
Classified as: pos (1.00)

Sentence: Niestety, mieliśmy dużego pecha i przegraliśmy
 - terms: 'pos' probability: 0.02; 'neg' probability: 0.98
Classified as: neg (0.98)

Sentence: Zachorowałem i leżę w łóżku
 - terms: 'pos' probability: 0.10; 'neg' probability: 0.90
Classified as: neg (0.90)

Sentence: To bardzo smutna wiadomość, nie mogę tego zrozumieć
 - terms: 'pos' probability: 0.04; 'neg' probability: 0.96
 - bigrams: 'pos' probability: 0.00; 'neg' probability: 1.00
 - trigrams: 'pos' probability: 0.00; 'neg' probability: 1.00
Classified as: neg (0.99)

Sentence: Zxcjhgoiu ooijasddnakjz zczxnzbxcz qdqdqqfefw sdsdfsdfsdf
Classified as: --- (1.00)

Sentence: Przystojniaczek! :-) :D :(
 - terms: 'pos' probability: 0.93; 'neg' probability: 0.07
 - emoticons: 'pos' probability: 0.67; 'neg' probability: 0.33
Classified as: pos (0.80)
```

## Measuring accuracy

```python
from src.emo_cls import EmoClassifier

if __name__ == '__main__':
   e = EmoClassifier(is_load_cached_cls=True)

   e.load_testset('data/testsets/test1.txt')
   print 'Accuracy: %s\n' % (e.accuracy())

   print 'Confusion matrix:'
   test_labels = [e.classify(sent)[0] for sent in e.test_set_sents]
   e.print_confusion_matrix(e.test_set_labels, test_labels)
```

Output:

```
0.818181818182

Confusion matrix:
    |  -  n  p |
    |  -  e  o |
    |  -  g  s |
----+----------+
--- | <1> .  . |
neg |  .<24> . |
pos |  .  6<19>|
----+----------+
(row = reference; col = test)
```
