from math import log10
from collections import Counter
from os.path import exists
from segment import clean, tk

_PATH = 'tfidf.txt'
discarded_flags = {'c', 'd', 'e', 'm', 'mq', 'o', 'p', 'r', 'u', 'y'}


def cut(text):
    for sentence in clean.ngram(text.strip()):
        for word in tk.cut(sentence):
            if clean.is_word(word) and tk.get_flag(word) not in discarded_flags:
                yield word


class TFIDF:
    def __init__(self, idf):
        self.idf = idf

    @classmethod
    def train(cls, texts):
        texts = [set(cut(text)) for text in texts]
        le = len(texts)
        words = set(w for t in texts for w in t)
        idf = {w: log10(le/(sum(1 if w in t else 0 for t in texts)+1))for w in words}
        return cls(idf)

    @classmethod
    def save_and_load(cls, texts=None, fname=_PATH):
        if exists(fname):
            idf = dict()
            with open(fname, encoding='utf-8') as fr:
                for line in fr.read().strip().split('\n'):
                    word, value = line.split()
                    idf[word] = float(value)
            return cls(idf)
        model = cls.train(texts)
        with open(fname, 'w', encoding='utf-8') as fw:
            for k, v in sorted(model.idf.items(), key=lambda x: x[1]):
                fw.write('%s %f\n' % (k, v))
        return model

    def get_idf(self, word):
        return self.idf.get(word, max(self.idf.values()))

    def extract(self, text, top_n=10, flags=False):
        counter = Counter()
        for w in cut(text):
            counter[w] += self.get_idf(w)
        if flags:
            return [(w, tk.get_flag(w)) for w, i in counter.most_common()]
        return [w for w, i in counter.most_common(top_n)]
