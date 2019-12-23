"""
基于jieba词库，进行修整

# 单字
^[^ ] \d\d [a-z]+\n
# 长词
^[^ ]{11} \d{1,} [a-z]+\n
# 数词
^[\u4e00-\u9fa5]{6,} \d+ m\n
^[\u4e00-\u9fa5]{2} [12] m\n
# 人名
^[\u4e00-\u9fa5]{2,} \d nrfg\n
^[\u4e00-\u9fa5]{1,2} \d\d nrfg\n
^[\u4e00-\u9fa5]{1,} \d nr\n
^[\u4e00-\u9fa5]{2} \d\d nr\n
^[\u4e00-\u9fa5]{2,3} \d nz\n
^[\u4e00-\u9fa5]{1,} \d nrt\n

# 词性
df -> d
dg -> d
h -> d
k -> n r
mg -> t
rg -> r
rr -> r
rz -> r
tg -> t
ud -> u
ug -> u
uj -> u
ul -> u
uv -> u
uz -> u
vd -> v
vq -> v
vi -> v
"""
import pandas as pd, pickle
from os import path

PATH_JIEBA = path.join(path.dirname(__file__), 'dict.txt')
PATH_DISTRICT = path.join(path.dirname(__file__), 'district.txt')  # 中国行政区划
GET_FREQ = lambda x: {1: 2000, 2: 300, 3: 40, 4: 5}.get(x, 2)
STOP_WORDS = set('''
了 是 在 和 有 他 我 的 也 为 就 这 都 等 着 来 与 要 又 而 一个 之 以 她 去 那 但 把 我们 可 他们 并 自己 或 由 其 给 使 却
这个 它 已经 及 这样 这些 此 们 这种 如果 因为 即 其中 现在 一些 以及 同时 由于 所以 这里 因 曾 呢 但是 该 每 其他 应 吧 虽然
因此 而且 啊 应该 当时 那么 这么 仍 还有 如此 既 或者 然后 有些 那个 关于 于是 不仅 只要 且 另外 而是 还是 此外 这次 如今 就是
并且 从而 其它 尽管 还要 即使 总是 只有 只是 而言 每次 这是 就会 那是'''.strip().split())


# 读


def txt2df(fname=PATH_JIEBA, sep=' ', names=None):
    """默认读取jieba词典"""
    return pd.read_table(fname, sep, names=names, header=None)


def sheet2df(fname, sheet_name=0):
    return pd.read_excel(fname, sheet_name=sheet_name)


def pickle2dt(fname):
    with open(fname, 'rb') as f:
        return pickle.load(f)


def txt2ls(fname=PATH_DISTRICT):
    with open(fname, encoding='utf-8') as f:
        return f.read().strip().split('\n')


def read_district():
    """
    读取中国行政区划，返回【编码、区划名称、区划等级、词性、区划上级】
    """
    exclusion = {'市辖区', '县', '省直辖县级行政区划', '自治区直辖县级行政区划', '城区', '郊区'}
    flags = {0: 'nation', 1: 'province', 2: 'city', 3: 'district'}
    code2region = dict()
    for line in txt2ls():
        code, region = line.split(',')
        code2region[code] = region
        level = int(len(code) / 2)
        flag = flags[level]
        if level < 2:
            superior = '中央' if level == 1 else ''
        else:
            superior = code2region[code[:level * 2 - 2]]
        if region not in exclusion:
            yield code, region, level, flag, superior


# 处理


def df2dt(df):
    assert df.shape[1] == 2
    return dict(df.values)


def ls2df(ls, columns):
    return pd.DataFrame(ls, columns=columns)


def insert_freq(df, column='word'):
    """插入【freq】列"""
    df['freq'] = df[column].str.len().apply(GET_FREQ)  # 字符串长度->分词概率
    return df


def insert_flag(df, flag):
    """插入【flag】列"""
    df['flag'] = flag
    return df


def concat(ls_of_df, freq=False):
    """合并DataFrame，按第0列去重，保留前者"""
    df = pd.concat(ls_of_df)
    if freq:  # 按freq降序
        df.sort_values(by='freq', ascending=False, inplace=True)
    return df.drop_duplicates(subset=df.columns[0])


# 写


def df2sheet(df, fname):
    fname = fname.replace('.xlsx', '') + '.xlsx'
    df.to_excel(fname, index=False)


def df2sheets(ls_of_df, sheet_names, fname):
    fname = fname.replace('.xlsx', '') + '.xlsx'
    excel_writer = pd.ExcelWriter(fname)
    for df, sheet_name in zip(ls_of_df, sheet_names):
        df.to_excel(excel_writer, sheet_name, index=False)
    excel_writer.save()


def dt2pickle(fname, dt):
    fname = fname.replace('.pickle', '') + '.pickle'
    with open(fname, 'wb') as f:
        pickle.dump(dt, f)


def ls2sheet(ls, columns=['word', 'flag', 'freq', 'bar'], fname='frequency'):
    df2sheet(ls2df(ls, columns), fname)


if __name__ == '__main__':
    print(txt2df())
