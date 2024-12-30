Fork自 https://github.com/rfg1024/GlossaryGenerator

如今AI大模型快速发展，本脚本相比较本地部署AI大模型或其VIP，几乎毫无先进性，哈哈。


## 原理

改用 `spacy` 库进行处理

1. 读取一本小说的文本，干掉复数、时态这些东西，得到一本小说的词汇表；
2. 和常用（高频）词库`dict`对比，去掉词库中排名前`num`个单词，生成你可能不认识的词表。

    目前预置词典有：

        - `COCA20000.txt`: COCA语料库20000词，高频排序
        - `collins.txt`: 柯林斯语料库14148词，高频排序
        - `common30k.txt`: 通常30000词，高频排序
        - `middleschool1600.txt`: 中国初中1600词，字母排序

生词表生成后可导入GoldenDict，欧陆词典一类app，快速预习一下，可以大幅提升阅读原版书籍时的体验。

## 依赖python库

参照`pyproject.toml`中内容。其中en-core-web-sm可能需科学上网。

``` toml
dependencies = [
    "textract-py3>=2.1.0",
    "spacy>=3.8.3",
    "en-core-web-sm @ https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl",
]
```


## 支持格式

- txt
- pdf（文字版）
- epub
- doc/docx
- csv
- xls
- xlsx

非txt文件花的时间会久一点，对其他格式的支持不一定好，我没有测试特别多文件。

## 使用方法

### 命令行方法

`generator.py -h`

```
usage: generator [-h] -f FILENAME [-d DICT_EXCLUDE] [-n NUM]

generator text glossaries

options:
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        The text filename (default: None)
  -d DICT_EXCLUDE, --dict-exclude DICT_EXCLUDE
                        Exclude the words from the dictionary (default:
                        middleschool1600.txt)
  -n NUM, --num NUM     Exclude the first n words from the dictionary。Special
                        Value：-1, All the words; 0, None of all (default: -1)

https://github.com/sd44/generator
```


### 函数方法

见`generator.py`，有详细注释。
