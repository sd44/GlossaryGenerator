#!/usr/bin/env python
# coding: utf-8

# # Glossary Generator

# 即兴想起来就写了，主要目的是配合英语学习的透析阅读法使用，什么叫透析阅读法请自行搜索。
#
# 程序比较简单，简单地说，就是：
# 1. 读取一本小说的文本，干掉复数、时态这些东西，得到一本小说的词汇表；
# 2. 和美国当代英语语料库COCA20000词频表对比，去掉特别高频的词和不常用的词，生成你可能不认识的词表。
#
# 生词表生成后可导入欧陆词典一类的app，快速预习一下，可以大幅提升阅读原版书籍时的体验。

import re
import string

import textract

# 目前支持txt/pdf/doc/docx/csv/epub格式，扫描版的PDF不行，只能是文字版的。
#
# 除了txt外，其他格式读取时花的时间会长一点，请耐心等待。

# filename = 'pride_and_prejudice.txt'
filename = '1984.txt'

# 读取文本，去掉标点符号。

byte = textract.process(filename)

text = byte.decode("utf-8")

text = text.translate(str.maketrans("—-", '  '))
text = re.sub(r'[0-9]', '', text)
text = text.translate(str.maketrans('', '', string.punctuation))

print("Reading text over!\n Now let's spacy")


import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)

wordset= set()

# token.text: 单词的原始形式。
# token.lemma_: 单词的基本形式（或词干）。例如，“running”的词干是“run”。
# token.pos_: 单词的粗粒度的词性标注，如名词、动词、形容词等。
# token.tag_: 单词的细粒度的词性标注，提供更多的语法信息。
# token.dep_: 单词在句子中的依存关系角色，例如主语、宾语等。
# token.shape_: 单词的形状信息，例如，单词的大小写，是否有标点符号等。
# token.is_alpha: 这是一个布尔值，用于检查token是否全部由字母组成。
# token.is_stop: 这是一个布尔值，用于检查token是否为停用词（如“the”、“is”等在英语中非常常见但通常不包含太多信息的词）。
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
            token.shape_, token.is_alpha, token.is_stop)
    if not token.is_stop and token.is_alpha:
        wordset.add(token.lemma_.lower())

wordset.add(token.lemma_)

# 统计词频，得到全部单词表。
# 这里我做了一点增强，将所有单词按出现频率由高到低排列。
#
# 对于一些学术性或专业性较强的文章，可能比较多词不在后面的常用词频表里，那么到这一步就可以了，跳过词频对比，直接写入一个文件，直接看看后面一部分单词即可。
#
# 另外我把最高频的1000词也去掉了，避免一些极其简单的词汇或标点符号的干扰。

# In[6]:

# word_count = collections.Counter(lemmatized_tokens)
# word_count = sorted(word_count.items(), key=lambda pair: pair[1], reverse=True)
# clean_words = [pair[0] for pair in word_count]
# len(clean_words)

known_words = open('middleschool1600.txt', 'r',
                   encoding='utf-8').read().replace('\n', ' ').split(' ')
known_words = set(known_words)

clean_words = wordset - known_words

# ## 美国当代英语语料库COCA
#
# 美国当代英语语料库（Corpus of Contemporary American English，简称COCA）是目前最大的免费英语语料库，它由包含5.2亿词的文本构成，这些文本由口语、小说、流行杂志、报纸以及学术文章五种不同的文体构成。从1990年至2015年间语料库以每年增加两千万词的速度进行扩充，以保证语料库内容的时效性。因此，美国当代英语语料库被认为是用来观察美国英语当前发展变化的最合适的英语语料库。
#
# 语料库的地址是：http://corpus.byu.edu/coca/
#
# 我这里用的是20200常用词，如果你英语水平较高，可以考虑去下载更大的词库来比对。

# ## 柯林斯词典词频
#
# 有一些反馈说COCA里口语比较多，所以我换了一下Collins词典的词频。Collins的词库里只有14000-15000单词，但我测试的效果似乎比COCA好一些。大家可以自己更改文件名，看看自己哪一个更合适。

# In[7]:

# dict_words = open('common30k.txt', 'r',
#                   encoding='utf-8').read().replace('\n', ' ').split(' ')
# dict_words = dict_words[3001:]

# 我附的高频词表是顺序的，即高频词在前，低频词在后。比对时我去掉了前面的2000常用词，如果你觉得自己词汇量低，可以考虑只去掉1000；反之亦然。

# In[8]:

# new_words = [w for w in clean_words if w in dict_words]
# len(new_words)

# 这个词表里肯定有很多还是你认识的，不过我觉得在生词本里过一遍（尤其是欧陆提供很多例句）看看怎么用还是有帮助的。如果认识的词特别多，请返回上面一步干掉更多高频词。我个人的小经验是阅读生词量在10%左右的小说学习+阅读体验比较好。
#
# 也可以考虑使用其他词频库来对比，比如Collins词频表。

# In[9]:

glossary = filename.split('.')[0] + '_glossary.txt'
with open(glossary, 'w') as output:
    output.write('\n'.join(clean_words))

# ## 不要死记硬背
#
# 还是忍不住多叨叨两句，很多人一学英语就想背单词，要是背了几次还记不住就抓狂焦虑。完全没有必要，通过阅读累积的词汇量更加牢固，一个单词在阅读中重复的次数够多你就会记住，不够多说明你暂时用不上，以后见多了再记是一样的。语言是工具，是获取信息的渠道，不要总是用考试的思维来衡量。
