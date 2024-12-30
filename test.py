import re
from nltk.tokenize import word_tokenize

# 示例文本
text = "Hello! This is an example text, with\n special\n symbols like @, #, $, etc."

# 去掉特殊符号（保留字母、数字和空格）
cleaned_text = re.sub(r'[^\w\s]', '', text)

# 分词
tokens = word_tokenize(cleaned_text)

print("原始文本:", text)
print("去掉特殊符号后的文本:", cleaned_text)
print("分词结果:", tokens)
