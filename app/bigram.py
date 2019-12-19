from collections import Counter
from pandas import DataFrame
from segment.corpus import STOP_WORDS
from segment import tk
from segment import clean

tk.add_re(clean.re_time, 'TIME')
N = 99999


def clear(text):
    text = clean.re_url.sub('', text)
    text = clean.re_email.sub('', text)
    text = clean.re_ip.sub('', text)
    return text


def trigram(texts, n=2, stop_words=STOP_WORDS):
    """统计语言模型"""
    c = Counter()
    for text in texts:
        for sentence in clean.ngram(clear(text)):
            words = [w for w in tk.cut(sentence) if w not in stop_words]
            for i in range(len(words) + 1 - n):
                c[' '.join(words[i: i + n])] += 1
    DataFrame(c.most_common(N), columns=['word', 'freq'])[['freq', 'word']].to_excel('%dgram.xlsx' % n, index=False)


def trigram_flag(texts, n=2, stop_words=STOP_WORDS):
    """统计语言模型（带词性）"""
    c = Counter()
    for text in texts:
        for sentence in clean.ngram(clear(text)):
            words = [w for w in tk.cut(sentence) if w not in stop_words]
            for i in range(len(words) + 1 - n):
                word = ' '.join(words[i: i + n])
                flag = ' '.join(tk.get_flag(w) for w in words[i: i + n])
                c[(word, flag)] += 1
    u = c.most_common()[0][1]
    c = [(i, j, k, tk.bar(k, u)) for (i, j), k in c.most_common(N)]
    DataFrame(c, columns=['word', 'flag', 'freq', 'bar']).to_excel('%dgram_flag.xlsx' % n, index=False)


def trigram_flag_sort(texts, n=2, stop_words=STOP_WORDS):
    """统计语言模型（带词性+排序）"""
    c = Counter()
    for text in texts:
        for sentence in clean.ngram(clear(text)):
            words = [w for w in tk.cut(sentence) if w not in stop_words]
            for i in range(len(words) + 1 - n):
                wf = sorted([(tk.get_flag(w), w) for w in words[i: i + n]])
                word = ' '.join(j[1] for j in wf)
                flag = ' '.join(j[0] for j in wf)
                c[(word, flag)] += 1
    c = [(k, j, i) for (i, j), k in c.most_common(N)]
    DataFrame(c, columns=['freq', 'flag', 'word']).to_excel('%dgram_flag_sort.xlsx' % n, index=False)


def trigram_flag_combo(texts, xrange=range(1, 4)):
    for n in xrange:
        trigram_flag(texts, n)

