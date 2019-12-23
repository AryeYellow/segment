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

## 词性

<table>
<tr>
<td>en</td><td>cn</td><td>e.g.</td>
</tr>
<tr>
<td>a</td><td>形容词</td><td>高 明 尖 诚 粗陋 冗杂 丰盛 顽皮 很贵 挺好用 …</td>
</tr>
<tr>
<td>ad</td><td>副形词</td><td>努目 完全 努力 切面 严实 慌忙 明确 仓惶 详细 …</td>
</tr>
<tr>
<td>ag</td><td>形语素</td><td>详 笃 睦 奇 洋 裸 渺 忤 虐 黢 怠 峻 悫 鄙 秀 …</td>
</tr>
<tr>
<td>an</td><td>名形词</td><td>麻生 猥琐 腐生 困苦 危难 负疚 刚愎 危险 悲苦 …</td>
</tr>
<tr>
<td>b</td><td>区别词</td><td>劣等 洲际性 超常规 同一性 年级 非农业 二合一 …</td>
</tr>
<tr>
<td>c</td><td>连词</td><td>再者说 倘 只此 或曰 以外 换句话说 虽是 除非 …</td>
</tr>
<tr>
<td>d</td><td>副词</td><td>幸免 四顾 绝对 急速 特约 从早 务须 逐行 挨边 …</td>
</tr>
<tr>
<td>e</td><td>叹词</td><td>好哟 嗄 天呀 哎 哇呀 啊哈 嗳 诶 嗬 呜呼 哇塞 …</td>
</tr>
<tr>
<td>f</td><td>方位词</td><td>内侧 以来 面部 后侧 面前 沿街 之内 两岸 里 …</td>
</tr>
<tr>
<td>g</td><td>语素</td><td>媸 璇 戬 瓴 踔 鳌 撄 絷 膑 遘 醢 槊 胂 鹎 豳 …</td>
</tr>
<tr>
<td>i</td><td>成语</td><td>绿荫蔽日 振耳欲聋 沧海一粟 一望无边 为尊者讳 …</td>
</tr>
<tr>
<td>j</td><td>简称略语</td><td>交警 中低收入 四个现代 经检测 青委 车改 常委 …</td>
</tr>
<tr>
<td>k</td><td>后接成分</td><td>型 者 式 们</td>
</tr>
<tr>
<td>l</td><td>习用语</td><td>不懂装懂 相聚一刻 由下而上 十字路口 查无此人 …</td>
</tr>
<tr>
<td>m</td><td>数词</td><td>九六 十二 半成 戊酉 俩 一二三四五 丙戌 片片 …</td>
</tr>
<tr>
<td>mq</td><td>数量词</td><td>半年度 四方面 十付 三色 一口钟 四面 三分钟 …</td>
</tr>
<tr>
<td>n</td><td>名词</td><td>男性 娇子 气压 写实性 联立方程 商业智能 寒窗 …</td>
</tr>
<tr>
<td>ng</td><td>名语素</td><td>诀 卉 茗 鹊 娃 寨 酊 钬 雹 役 莺 谊 隙 族 鸩 …</td>
</tr>
<tr>
<td>nr</td><td>人名</td><td>雍正皇帝 小老弟 唐僧骑 铁娘子 川军 小甜甜 璐 …</td>
</tr>
<tr>
<td>nrfg</td><td>人名</td><td>聂远 懊悔无及 袁咏仪 李自成起义 鸣叫声 金日成 …</td>
</tr>
<tr>
<td>nrt</td><td>外国人名</td><td>米尔科 达尼丁 三世 五丁 塞拉 埃克尔斯 贝当 …</td>
</tr>
<tr>
<td>ns</td><td>地名</td><td>南明 锡山 拱北 南非 哥里 平北 丹井 佛山 广州 …</td>
</tr>
<tr>
<td>nt</td><td>机构团体</td><td>浙江队 中医院 中华网 铁道部 广电部 联想集团 …</td>
</tr>
<tr>
<td>nz</td><td>其他专名</td><td>培根 补丁 圣战士 英属 三民主义 国药准字 …</td>
</tr>
<tr>
<td>o</td><td>拟声词</td><td>哈喇 咝 哗喇 咔喳 飕 哇哇 喃 咕隆 咿呀 唧咕 …</td>
</tr>
<tr>
<td>p</td><td>介词</td><td>顺当 顺着 借了 连着 乘着 除了 较之于 根 自 …</td>
</tr>
<tr>
<td>q</td><td>量词</td><td>毫厘 盅 封 千瓦小时 立方米 盎 座 毫克 张 斛 …</td>
</tr>
<tr>
<td>r</td><td>代词</td><td>该车 这时 那些 甚么 鄙人 此案 睿智者 他 怎生 …</td>
</tr>
<tr>
<td>s</td><td>处所词</td><td>世外 肩前 舷外 手下 耳边 兜里 盘头 桌边 家外 …</td>
</tr>
<tr>
<td>t</td><td>时间词</td><td>新一代 清时 先上去 月初 昔年 无日 唐五代 佳日 …</td>
</tr>
<tr>
<td>u</td><td>助词</td><td>则否 等 恁地 等等 似的 来说 矣哉 来看 般 的话 …</td>
</tr>
<tr>
<td>v</td><td>动词</td><td>批发 孕育 作成 纳闷儿 遭殃 留话 吻下去 创生 …</td>
</tr>
<tr>
<td>vg</td><td>动语素</td><td>悖 谏 踞 泯 濯 掳 诌 疑 诲 吁 囿 酌 蟠 豢 匿 …</td>
</tr>
<tr>
<td>vn</td><td>名动词</td><td>审查 相互毗连 销蚀 反动 对联 劳工 漫游 监押 …</td>
</tr>
<tr>
<td>x</td><td>非语素字</td><td>舭 珑 婪 躅 蕺 蜓 螂 窀 蘅 葜 姆 榍 虺 楂 龊 …</td>
</tr>
<tr>
<td>y</td><td>语气词</td><td>吓呆了 呃 呀 兮 哩 呐 嘞 哇 呗 意谓着 也罢 啦 …</td>
</tr>
<tr>
<td>z</td><td>状态词</td><td>歪曲 飘飘 慢慢儿 急地 沉迷在 医疗纠纷 晕呼呼 …</td>
</tr>
<tr>
<td>zg</td><td></td><td>鮛 瑑 灘 鄼 緣 嗙 獘 洅 暠 埄 涚 鞞 檺 肸 撻 …</td>
</tr>
</table>



