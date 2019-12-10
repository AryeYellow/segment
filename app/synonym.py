from os.path import exists
from gensim.models import Word2Vec
from collections import Counter
from segment import clean, tk, corpus
_path_w2v = ''
_path_counter = ''
size = 100
window = 10
sg = 1  # skip-gram
flag_filter = {'d', 'e', 'h', 'k', 'm', 'mq', 'o', 'p', 'r', 'u', 'y', 'NUM'}


def get_flag(word):
    if word in corpus.STOP_WORDS:
        return False
    flag = tk.get_flag(word)
    if flag in flag_filter:
        return False
    return True


def clean_text(text):
    text = clean.re_url.sub('', text)
    text = clean.re_email.sub('', text)
    text = clean.re_ip.sub('', text)
    text = clean.replace_space(text)
    text = clean.replace_punctuation(text)
    text = clean.re_time.sub('TIME', text)
    return text


def texts2sentences(texts):
    # return [[w for w in tk.cut(clean_text(t)) if get_flag(w)] for t in texts]
    return [[w for w in tk.cut(p) if get_flag(w)] for t in texts for p in clean.text2sentence(clean_text(t))]


def modeling(sentences, cut=texts2sentences, model_path='word2vec', loop=False):
    """词向量建模"""
    if not exists(model_path):
        if cut:
            sentences = cut(sentences)
        Word2Vec(sentences, size=size, window=window, sg=sg).save(model_path)
    wv = Word2Vec.load(model_path).wv
    while loop:
        loop = input('相似词模型：').strip()
        try:
            for word, similarity in wv.similar_by_word(loop, 15):
                tk.bar(similarity, 1, word)
        except KeyError:
            pass
    counter = Counter(w for s in sentences for w in s)
    return wv, counter


def synonym_w2v(texts, words):
    for word in words:
        tk.add_word(word, flag='TEMP')
    wv, counter = modeling(texts, loop=False)
    standard = counter.most_common()[0][1] ** .5
    ls_of_df = []
    for word in words:
        try:
            ls = [(w, tk.get_flag(w), s, counter[w], tk.bar(counter[w]**.5, standard))
                  for w, s in wv.similar_by_word(word, 100)]
        except KeyError:
            continue
        ls_of_df.append(corpus.ls2df(ls, ['word', 'flag', 'similar', 'frequency', 'bar']))
    corpus.df2sheets(ls_of_df, [clean.re.sub('\W', '', w)for w in words], 'synonym_w2v')


def synonym_bigram(texts, center_word, filtrate=get_flag):
    """组合词"""
    tk.add_word(center_word, 2000, 'CENTER')
    left, right = Counter(), Counter()
    for text in texts:
        if center_word in text:
            for sentence in clean.ngram(text):
                words = [w for w in tk.cut(sentence) if filtrate(w)]
                for i in range(len(words) - 1):
                    if words[i] == center_word:
                        word = ' '.join(words[i: i + 2])
                        flag = ' '.join(tk.get_flag(w) for w in words[i: i + 2])
                        left[(word, flag)] += 1
                    if words[i + 1] == center_word:
                        word = ' '.join(words[i: i + 2])
                        flag = ' '.join(tk.get_flag(w) for w in words[i: i + 2])
                        right[(word, flag)] += 1
    u = max(left.most_common()[0][1], right.most_common()[0][1])
    left = corpus.ls2df([(i, j, k, tk.bar(k, u)) for(i, j), k in left.most_common()], ['word', 'flag', 'freq', 'bar'])
    right = corpus.ls2df([(i, j, k, tk.bar(k, u)) for(i, j), k in right.most_common()], ['word', 'flag', 'freq', 'bar'])
    corpus.df2sheets([left, right], ['left', 'right'], 'synonym_bigram_%s.xlsx' % center_word)


def _edit_dist_step(lev, i, j, s1, s2, transpositions=False):
    c1 = s1[i - 1]
    c2 = s2[j - 1]
    # skipping a character in s1
    a = lev[i - 1][j] + 1
    # skipping a character in s2
    b = lev[i][j - 1] + 1
    # substitution
    c = lev[i - 1][j - 1] + (1 if c1 != c2 else 0)
    # transposition
    d = c + 1  # never picked by default
    if transpositions and i > 1 and j > 1:
        if s1[i - 2] == c2 and s2[j - 2] == c1:
            d = lev[i - 2][j - 2] + 1
    # pick the cheapest
    lev[i][j] = min(a, b, c, d)


def edit_distance(s1, s2, transpositions=False):
    # set up a 2-D array
    len1 = len(s1) + 1
    len2 = len(s2) + 1
    lev = []
    for i in range(len1):
        lev.append([0] * len2)  # initialize 2D array to zero
    for i in range(len1):
        lev[i][0] = i  # column 0: 0,1,2,3,4,...
    for j in range(len2):
        lev[0][j] = j  # row 0: 0,1,2,3,4,...
    # iterate over the array
    for i in range(len1 - 1):
        for j in range(len2 - 1):
            _edit_dist_step(lev, i+1, j+1, s1, s2, transpositions)
    return lev[-1][-1]


def synonym_ed(texts, word, cut=clean.text2phrase):
    len_w = len(word) - 1
    c = Counter()
    for text in texts:
        for phrase in cut(text):
            len_p = len(phrase)
            for i in range(len_p - len_w):
                if edit_distance(word, phrase[i: i + len_w]) == 1:
                    c[phrase[i: i + len_w]] += 1
            for i in range(len_p - len_w - 1):
                if edit_distance(word, phrase[i: i + len_w + 1], transpositions=True) <= 1:
                    c[phrase[i: i + len_w + 1]] += 1
            for i in range(len_p - len_w - 2):
                if edit_distance(word, phrase[i: i + len_w + 2]) == 1:
                    c[phrase[i: i + len_w + 2]] += 1
    u = c.most_common()[0][1]
    corpus.ls2sheet([(w, len(w), f, tk.bar(f, u)) for w, f in c.most_common()],
                    ['word', 'len', 'freq', 'bar'], 'synonym_ed_%s.xlsx' % word)
    for w, f in reversed(c.most_common()):
        tk.bar(f, u, w)
