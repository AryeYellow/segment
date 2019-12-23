import re
from collections import Counter
from pandas import DataFrame
from segment import clean
from segment.hmm import tk as tk1
from segment.hmm_flag import tk as tk2

dictionary = set(tk1.word2flag)
tk1.add_re(re.compile('[a-z0-9_-]', re.I), 'ENUM')
N = 99999


def new_word(texts, fname='new_word.xlsx'):
    """探索新词"""
    c = Counter(
        w for t in texts for s in clean.ngram(t) for w in tk1.cut(s)
        if clean.is_word(w) and w not in dictionary).most_common(N)
    DataFrame(c, columns=['word', 'freq']).to_excel(fname, index=False)
    maximum = c[0][1] ** .5
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, w)


def new_word_flag(texts, fname='new_word_flag.xlsx'):
    """探索新词极其词性"""
    c = Counter(
        (w.word, w.flag) for t in texts for s in clean.ngram(t) for w in tk2.cut(s)
        if clean.is_word(w.word) and w.word not in dictionary).most_common(N)
    maximum = c[0][1] ** .5
    DataFrame([(i, j, k, tk2.bar(k**.5, maximum)) for (i, j), k in c],
              columns=['word', 'flag', 'freq', 'bar']).to_excel(fname, index=False)
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, ' '.join(w))


def frequency(texts, fname='frequency.xlsx'):
    """词频统计"""
    c = Counter(w for t in texts for s in clean.ngram(t) for w in tk1.cut(s)if clean.is_word(w)).most_common(N)
    DataFrame([(w, tk1.get_flag(w), f)for w, f in c], columns=['word', 'flag', 'freq']).to_excel(fname, index=False)
    maximum = c[0][1] ** .5
    for w, f in reversed(c):
        tk1.bar(f**.5, maximum, w)

