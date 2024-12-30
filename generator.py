#!/usr/bin/env python3
"""生成文本单词表，fork自https://github.com/rfg1024/GlossaryGenerator

Examples:
    books目录下存有三本书的txt文件，生成其单词表::

        print('Now glossaries The Old Man and the Sea')
        get_glossaries('books/oldmanandthesea.txt', 'collins.txt', 3000)

        print('Now glossaries Pride and Prejudice')
        get_glossaries('books/pride_and_prejudice.txt', 'COCA20000.txt', 5000)

        print('Now glossaries 1984')
        get_glossaries('books/1984.txt')


"""

import argparse
import re
from pathlib import PurePath

import textract


def read_file(filename):
    """ 从 txt/文字版pdf/doc/docx/csv/epub格式文件中读取文字

    Note:
        依赖于 ``textract``

        除了txt外，其他格式读取时花的时间会长一点，请耐心等待。

        books目录下有三本例书 pride_and_prejudice.txt 1984.txt oldmanandthesea.txt

    """
    byte = textract.process(filename)

    text = byte.decode("utf-8")

    print("Reading text over!")
    return text


def spacy_lemma(text):
    """ 使用spacy进行词干还原

    Note:
        依赖于 ``spacy``

        请先安装spacy，然后下载英文模型:

        .. code-block:: bash

            pip install spacy
            python -m spacy download en_core_web_sm

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
        if token.is_alpha and not token.is_stop:
            wordset.add(token.lemma_.lower())

    return wordset


def clean_word(wordset, known_word_file='middleschool1600.txt', known_lens=-1):
    known_words = open(known_word_file, 'r',
                       encoding='utf-8').read().replace('\n', ' ').split(' ')
    if known_lens == -1:
        known_lens = len(known_words)
    known_words = set(known_words[:known_lens])
    known_words.update(
        set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'))

    clean_words = sorted(wordset - known_words)
    print(f'生成单词表数量{len(clean_words)}个')
    return clean_words


def get_glossaries(filename,
                   known_word_file='middleschool1600.txt',
                   known_lens=-1):
    """在当前目录生成文本单词表，取差集（去掉已在单词列表 ``known_word_file``
    中出现的前``known_lens``个数量的单词）。

    Args:
        filename (str): 要生成单词表的文件名
        known_word_file (str): 已知单词列表文件名. 预设了:
            - ``COCA20000.txt``: COCA语料库20000词，高频排序
            - ``collins.txt``: 柯林斯语料库14148词，高频排序
            - ``common30k.txt``: 通常30000词，高频排序
            - ``middleschool1600.txt``: 中国初中1600词，字母排序

        known_lens (int): 从已知单词列表中取前多少个单词。默认值为0，选取所有的单词。

    Note:
        生成的单词表以 ``_glossary.txt`` 结尾，如 ``1984_glossary.txt``

    """
    wordset = spacy_lemma(read_file(filename))
    cleanwords = clean_word(wordset, known_word_file, known_lens)

    glossary = PurePath(filename).stem + '_glossary.txt'
    with open(glossary, 'w') as output:
        output.write('\n'.join(cleanwords))
    print('Glossary generated:', glossary, '\n\n')


def main():

    # 定义一个ArgumentParser实例:
    parser = argparse.ArgumentParser(
        prog='generator',
        description='generator text glossaries',
        epilog='https://github.com/sd44/generator',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('-f',
                        '--filename',
                        type=str,
                        required=True,
                        help='The text filename')
    parser.add_argument('-d',
                        '--dict-exclude',
                        default='middleschool1600.txt',
                        type=str,
                        help="Exclude the words from the dictionary")
    parser.add_argument(
        '-n',
        '--num',
        default=-1,
        type=int,
        help=
        "Exclude the first n words from the dictionary。Special Value：-1, All the words; 0, None of all"
    )

    args = parser.parse_args()
    get_glossaries(args.filename, args.dict_exclude, args.num)


if __name__ == '__main__':
    main()
