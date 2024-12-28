#!/usr/bin/env python
# coding: utf-8

# # Glossary Generator

# 即兴想起来就写了，主要目的是配合英语学习的透析阅读法使用，什么叫透析阅读法请自行搜索。
#
# 程序比较简单，简单地说，就是：
# 1. 读取一本小说的文本，干掉复数、时态这些东西，得到一本小说的词汇表；
# 2. 和已知单词词表对比，去掉已知词，生成你可能不认识的词表。
#
# 生词表生成后可导入欧陆词典一类的app，快速预习一下，可以大幅提升阅读原版书籍时的体验。

import re
import string
from pathlib import PurePath

import textract


def read_file(filename):
    """ 从 txt/文字版pdf/doc/docx/csv/epub格式文件中读取文字，去除标点符号。

    Note:
        依赖于 ``textract``

        除了txt外，其他格式读取时花的时间会长一点，请耐心等待。

        books目录下有三本例书 pride_and_prejudice.txt 1984.txt oldmanandthesea.txt
    """
    byte = textract.process(filename)

    text = byte.decode("utf-8")

    text = text.translate(str.maketrans("—", ' '))
    text = re.sub(r'[0-9]', '', text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    print("Reading text over!\n")
    return text


def spacy_lemma(text):
    """ 使用spacy进行词干还原

    Note:
        依赖于 ``spacy``

        请先安装spacy，然后下载英文模型：
        ```
        pip install spacy
        python -m spacy download en_core_web_sm
        ```
    """
    import spacy

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    wordset = set()

    # token.text: 单词的原始形式。
    # token.lemma_: 单词的基本形式（或词干）。例如，“running”的词干是“run”。
    # token.pos_: 单词的粗粒度的词性标注，如名词、动词、形容词等。
    # token.tag_: 单词的细粒度的词性标注，提供更多的语法信息。
    # token.dep_: 单词在句子中的依存关系角色，例如主语、宾语等。
    # token.shape_: 单词的形状信息，例如，单词的大小写，是否有标点符号等。
    # token.is_alpha: 这是一个布尔值，用于检查token是否全部由字母组成。
    # token.is_stop: 这是一个布尔值，用于检查token是否为停用词（如“the”、“is”等在英语中非常常见但通常不包含太多信息的词）。
    for token in doc:
        # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
        #         token.shape_, token.is_alpha, token.is_stop)
        if token.is_alpha and not token.is_stop:
            wordset.add(token.lemma_.lower())

    return wordset


def clean_word(wordset, known_word_file='middleschool1600.txt', known_lens=0):
    known_words = open(known_word_file, 'r',
                       encoding='utf-8').read().replace('\n', ' ').split(' ')
    if known_lens == 0:
        known_lens = len(known_words)
    known_words = set(known_words[:known_lens])
    known_words.update(
        set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    clean_words = sorted(wordset - known_words)
    return clean_words


def get_glossaries(filename,
                   known_word_file='middleschool1600.txt',
                   known_lens=0):
    wordset = spacy_lemma(read_file(filename))
    cleanwords = clean_word(wordset, known_word_file, known_lens)

    glossary = PurePath('filename').stem + '_glossary.txt'
    with open(glossary, 'w') as output:
        output.write('\n'.join(cleanwords))


if __name__ == '__main__':
    print('Now glossaries 1984')
    get_glossaries('1984.txt')

    print('Now glossaries The Old Man and the Sea')
    get_glossaries('oldmanandthesea.txt', 'collins.txt', 3000)

    print('Now glossaries Pride and Prejudice')
    get_glossaries('pride_and_prejudice', 'COCA20000.txt', 5000)
