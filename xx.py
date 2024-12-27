
import spacy

nlp = spacy.load("en_core_web_sm")

text = "I love natural language processing."

doc = nlp(text)

for token in doc:
    print(token.text, token.pos_)

# 获取词形还原结果
def get_lemmatization(word_list):
    lemmatized_list = []
    for word in word_list:
        doc = nlp(word)
        lemmatized_word = doc[0].lemma_
        lemmatized_list.append(lemmatized_word)
    return lemmatized_list


test_word_list = ["men", "computers", "ate", "running", "fancier"]
result_word_list = get_lemmatization(test_word_list)
print(result_word_list)

from nltk.stem import SnowballStemmer

# 选择语言，创建实例
stemmer = SnowballStemmer("english")

test_word_list = ["running", "jumped", "eating", "playing"]
stemmed_words = [stemmer.stem(word) for word in test_word_list]

print(stemmed_words)

