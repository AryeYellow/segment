import re


def is_string(text):
    if isinstance(text, str):
        return text.strip()
    return ''


def are_strings(texts):
    for text in texts:
        text = is_string(text)
        if text:
            yield text


def replace_tag(html):
    """替换HTML标签"""
    # 独立元素
    html = re.sub('<br/?>|<hr/?>', '\n', html)  # 换行、水平线
    html = re.sub('&(nbsp|e[mn]sp|thinsp|zwn?j|#13);', ' ', html)  # 空格
    html = re.sub('<img[^>]*>', '', html)  # 图片
    html = re.sub('<!--[\s\S]*?-->', '', html)  # 注释
    html = re.sub('<style[^>]*>[\s\S]*?</style>', '', html)  # 样式
    html = re.sub('<script[^>]*>[\s\S]*?</script>', '', html)  # JavaScript
    html = html.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&amp;', '&')  # 转义字符
    # 行内元素
    html = re.sub('<b>([\s\S]*?)</b>', lambda x: x.group(1), html)  # 粗体 bold
    html = re.sub('<u>([\s\S]*?)</u>', lambda x: x.group(1), html)  # 下划线 underline
    html = re.sub('<strong>([\s\S]*?)</strong>', lambda x: x.group(1), html)  # 粗体
    html = re.sub('<i>([\s\S]*?)</i>', lambda x: x.group(1), html)  # 斜体 italic
    html = re.sub('<mark[^>]*>([\s\S]*?)</mark>', lambda x: x.group(1), html)  # 背景填充
    html = re.sub('<em>([\s\S]*?)</em>', lambda x: x.group(1), html)  # 强调 emphasize
    html = re.sub('<font[^>]*>([\s\S]*?)</font>', lambda x: x.group(1), html)  # 字体
    html = re.sub('<a[^>]*>([\s\S]*?)</a>', lambda x: x.group(1), html)  # a：超链接
    html = re.sub('<span[^>]*>([\s\S]*?)</span>', lambda x: x.group(1), html)  # span
    # 块级元素
    html = re.sub('<p[^>]*>([\s\S]*?)</p>', lambda x: '%s\n' % x.group(1), html)  # 段落
    html = re.sub('<h[1-6][^>]*>([\s\S]*?)</h[1-6]>', lambda x: '%s\n' % x.group(1), html)  # 标题
    html = re.sub('<td[^>]*>([\s\S]*?)</td>', lambda x: ' %s ' % x.group(1), html)  # 表格
    html = re.sub('<tr[^>]*>([\s\S]*?)</tr>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub('<th[^>]*>([\s\S]*?)</th>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub('<tbody[^>]*>([\s\S]*?)</tbody>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub('<table[^>]*>([\s\S]*?)</table>', lambda x: '%s\n' % x.group(1), html)  # 表格
    html = re.sub('<li[^>]*>([\s\S]*?)</li>', lambda x: '%s\n' % x.group(1), html)  # 列表
    html = re.sub('<[ou]l[^>]*>([\s\S]*?)</[ou]l>', lambda x: '%s\n' % x.group(1), html)  # 列表
    html = re.sub('<pre[^>]*>([\s\S]*?)</pre>', lambda x: '%s\n' % x.group(1), html)  # 预格化，可保留连续空白符
    html = re.sub('<div[^>]*>([\s\S]*?)</div>', lambda x: '%s\n' % x.group(1), html)  # 分割 division
    html = re.sub('<section[^>]*>([\s\S]*?)</section>', lambda x: '%s\n' % x.group(1), html)  # 章节
    # 剩余标签
    html = re.sub('<[^>]*>', '', html)
    html = re.sub('<[^>\u4e00-\u9fa5]+>', '', html)
    return html


def replace_punctuation(text):
    """替换标点（英→中）"""
    text = text.replace('(', '（').replace(')', '）')  # 圆括号
    text = text.replace('【', '（').replace('】', '）')  # 方括号（后用于关键词高亮）
    text = re.sub('[;；]+', '；', text)  # 分号
    text = re.sub('[!！]+', '！', text)  # 叹号
    text = re.sub('[?？]+', '？', text)  # 问号
    text = re.sub('[.]{3,}|,{3,}|。{3,}|，{3,}|…+', '…', text)  # 省略号
    text = text.replace("'", '"')  # 引号
    text = re.sub('(?<=[\u4e00-\u9fa5]),(?=[\u4e00-\u9fa5])', '，', text)  # 逗号
    text = re.sub('(?<=[\u4e00-\u9fa5])[.](?=[\u4e00-\u9fa5])', '。', text)  # 句号
    return text.strip().lower()  # 转小写


def replace_space(text):
    """清除连续空白"""
    text = re.sub('\s*\n\s*', '\n', text.strip())
    text = re.sub('[ \f\r\t　]+', ' ', text)
    text = re.sub('([\u4e00-\u9fa5]) ([^\u4e00-\u9fa5])', lambda x: x.group(1)+x.group(2), text)
    text = re.sub('([^\u4e00-\u9fa5]) ([\u4e00-\u9fa5])', lambda x: x.group(1)+x.group(2), text)
    return text


def replace_space_resolutely(text, substitution=''):
    return re.sub('\s+', substitution, text.strip())


def replace_empty_bracket(text):
    return re.sub('\[\]|【】|（）|\(\)|{}|<>', '', text)


sep10 = re.compile('[\n。…；;]+|(?<=[\u4e00-\u9fa5])[.]+(?=[\u4e00-\u9fa5])').split
sep15 = re.compile('[\n。…；;!！?？]+|(?<=[a-z\u4e00-\u9fa5])[.]+(?=[a-z\u4e00-\u9fa5])', re.I).split
sep20 = re.compile('[!！?？]+').split
sep30 = re.compile('[,，:：]+').split
sep40 = re.compile('[^a-zA-Z0-9\u4e00-\u9fa5]+').split
sep45 = re.compile('[^a-zA-Z\u4e00-\u9fa5]+').split
sep_cn = re.compile(
    '^ ?[0-9]{1,2}、|'
    '^ ?[0-9]{1,2}[.](?=[^0-9])|'
    '^ ?[一二三四五六七八九十]{1,3}、|'
    '^ ?（[一二三四五六七八九十]{1,3}）|'
    '^ ?第[一二三四五六七八九十]{1,3}章').split


def text2sentence(text):
    for i in sep10(text.strip()):
        if i.strip():
            yield i.strip()


def sentence2clause(sentence):
    for i in sep20(sentence.strip()):
        if i.strip():
            yield i.strip()


def clause2phrase(clause):
    for i in sep30(clause.strip()):
        if i.strip():
            yield i.strip()


def ngram(text):
    for i in sep40(text.strip()):
        if i.strip():
            yield i.strip()


def text2clause(text):
    for clause in sep15(text):
        clause = clause.strip()
        if clause:
            yield clause


def text2phrase(text):
    for sentence in sep15(text):
        for phrase in sep30(sentence):
            phrase = phrase.strip()
            if phrase:
                yield phrase


re_time = re.compile('[0-9]+([天年月日时分秒°]|小时|分钟|毫秒|时辰)+[0-9天年月日时分秒]*')
re_ymd = re.compile(
    '((19|20)[0-9]{2}年(0?[1-9]|1[012])月(0?[1-9]|[12][0-9]|3[01])日)|'
    '((19|20)[0-9]{2}-(0?[1-9]|1[012])-(0?[1-9]|[12][0-9]|3[01]))|'
    '((19|20)[0-9]{2}/(0?[1-9]|1[012])/(0?[1-9]|[12][0-9]|3[01]))')
re_md = re.compile('(?<![0-9])(0?[1-9]|1[012])月(0?[1-9]|[12][0-9]|3[01])日')
re_ym = re.compile('(?<![0-9])(19|20)[0-9]{2}年(0?[1-9]|1[012])月')
re_url = re.compile('[a-z]+(://|\.)[\w-]+(\.[a-z0-9_-]+)+[0-9a-z!%&()*./:=?_~,@^+#-]*', re.I)
re_email = re.compile('[a-z0-9]+@[a-z0-9_-]+(\.[0-9a-z!%&()*./:=?_~,@^+#-]+)+', re.I)
re_ip = re.compile('\d+\.\d+\.\d+\.\d+')
re_phone = re.compile('([0-9]{3,4}-|86+)?[0-9]{6,}')  # 电话、邮编、编号等


if __name__ == '__main__':
    pass
