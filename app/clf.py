"""
新闻9分类

1987 car
1961 education
1910 entertainment
1909 fashion
1996 finance
1906 military
1925 politics
1960 science
1989 sports
总数：17543
测试集切分比例：0.25

模型 | 准确率 | 秒
MultinomialNB | 0.8201 | 0.13
LogisticRegression | 0.8518 | 25.44
DecisionTreeClassifier | 0.7321 | 18.93
AdaBoostClassifier | 0.6979 | 23.44
GradientBoostingClassifier | 0.8381 | 793.17
RandomForestClassifier | 0.8399 | 129.67
SVC | 0.8450 | 492.10
"""
from collections import Counter
from numpy import argmax
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from segment import tk, clean, corpus
from warnings import filterwarnings
filterwarnings('ignore')  # 不打印警告

N = 20000


def clear(text):
    text = clean.re_url.sub('', text)
    text = clean.re_email.sub('', text)
    text = clean.re_ip.sub('', text)
    text = clean.replace_punctuation(text)
    # text = clean.re_time.sub('TIME', text)
    return clean.sep45(text)


def cut(text):
    for sentence in clear(text):
        for word in tk.cut(sentence):
            word = word.strip()
            if word not in corpus.STOP_WORDS and word != '':
                yield word


def clf_word(texts, labels, model=MultinomialNB, detail=False):
    # 向量化
    vectorizer = TfidfVectorizer(tokenizer=cut)
    x = vectorizer.fit_transform(texts)
    # 建模
    clf = model()
    clf.fit(x, labels)
    classes = clf.classes_
    print(model.__name__, clf.score(x, labels), *classes)
    # 词分类
    c = Counter(w for t in texts for w in cut(t)).most_common(N)
    if detail is False:
        ls = []
        for word, freq in c:
            flag = tk.get_flag(word)  # 词性
            predict_proba = clf.predict_proba(vectorizer.transform([word]))[0]
            max_index = argmax(predict_proba)
            max_proba = predict_proba[max_index]  # 概率
            label = classes[max_index]  # 类别
            ls.append([freq, flag, word, label, max_proba, tk.bar(max_proba)])
        corpus.ls2sheet(ls, ['freq', 'flag', 'word', 'label', 'probability', 'bar'], 'clf_word')
    else:
        maximum = c[0][1] ** .5
        ls = []
        for word, freq in c:
            flag = tk.get_flag(word)  # 词性
            predict_proba = clf.predict_proba(vectorizer.transform([word]))[0]  # 概率
            label = classes[argmax(predict_proba)]  # 类别
            ls.append([flag, word, label, *predict_proba, freq, tk.bar(freq**.5, maximum)])
        corpus.ls2sheet(ls, ['flag', 'word', 'label', *clf.classes_, 'freq', 'bar'], 'clf_word_detail')
        for i in reversed(ls):
            print(i[1], i[2], i[-1])


def clf_text(X, y):
    # 数据切分
    X_train, X_test, y_train, y_test = train_test_split(X, y)
    # 向量化
    vectorizer = TfidfVectorizer(tokenizer=cut)
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)
    # 建模
    for model in [MultinomialNB, LogisticRegression]:
        t0 = tk.second
        clf = model()
        clf.fit(X_train, y_train)
        print(model.__name__, tk.hot(clf.score(X_test, y_test)), tk.second-t0)
