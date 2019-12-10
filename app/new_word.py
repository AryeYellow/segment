from collections import Counter
from re import compile, I
from pandas import DataFrame
from segment.clean import ngram
from segment.hmm import tk as tk1
from segment.hmm_flag import tk as tk2

_dict = set(tk1.word2flag)
fullmatch = compile('[a-z0-9\u4e00-\u9fa5]*[a-z\u4e00-\u9fa5][a-z0-9\u4e00-\u9fa5]*', I).fullmatch
N = 99999


def new_word(texts, dictionary=_dict, fname='new_word.xlsx'):
    """探索新词"""
    c = Counter(
        w for t in texts for s in ngram(t) for w in tk1.cut(s)
        if len(w) > 1 and w not in dictionary and fullmatch(w)).most_common(N)
    DataFrame(c, columns=['word', 'freq']).to_excel(fname, index=False)
    maximum = c[0][1] ** .5
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, w)


def new_word_flag(texts, dictionary=_dict, fname='new_word_flag.xlsx'):
    """探索新词极其词性"""
    c = Counter(
        (w.word, w.flag) for t in texts for s in ngram(t) for w in tk2.cut(s)
        if len(w.word) > 1 and w.word not in dictionary and fullmatch(w.word)).most_common(N)
    maximum = c[0][1] ** .5
    DataFrame([(i, j, k, tk2.bar(k**.5, maximum)) for (i, j), k in c],
              columns=['word', 'flag', 'freq', 'bar']).to_excel(fname, index=False)
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, ' '.join(w))


def frequency(texts, fname='frequency.xlsx'):
    """词频统计"""
    c = Counter(w for t in texts for s in ngram(t) for w in tk1.cut(s) if fullmatch(w)).most_common(N)
    DataFrame([(w, tk1.get_flag(w), f) for w, f in c], columns=['word', 'flag', 'freq']).to_excel(fname, index=False)
    maximum = c[0][1] ** .5
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, w)

