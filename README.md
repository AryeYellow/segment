# 中文自然语言处理

## 工程架构
- **app** 应用
    - `bigram.py` 统计语言模型
    - `new_word.py` 新词探索
    - `synonym.py` 近义词探索
- **corpus** 语料库
    - `__init__.py` 语料读写工具
    - `city.py` 中国行政区划（省市）
    - `dict.txt` 通用词库
    - `district.txt` 中国行政区划（省市区）
- **hmm** 隐马尔科夫模型
    - `__init__.py` HMM分词模型接口
    - `prob_emit.py` 发射概率
- **hmm_flag** 带词性的隐马尔科夫模型
    - `__init__.py` 带词性HMM分词模型接口
    - `char_state_tab.py` 中文字符在BMES时对应的词性
    - `prob_emit.py` 发射概率
    - `prob_start.py` 起始概率
    - `prob_trans.py` 转移概率
- `__init__.py`中文分词接口
- `clean.py` 文本清洗
- `conf.py` 可视化、计时器

## 依赖
- pandas
- gensim
- sklearn

