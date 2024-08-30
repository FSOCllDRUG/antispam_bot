import pandas as pd
import string
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import json

# import nltk

# Загрузка необходимого ресурса
# nltk.download('punkt_russian')
# nltk.download('punkt_tab')
# nltk.download('stopwords')

# Загрузка данных из CSV файла
df = pd.read_csv('../data/spam_messages.csv')

# Предобработка данных
def preprocess_text(text):
    text = text.lower()  # Преобразование в нижний регистр
    text = text.translate(str.maketrans('', '', string.punctuation))  # Удаление знаков препинания
    tokens = word_tokenize(text)  # Токенизация
    tokens = [word for word in tokens if word not in stopwords.words('russian')]  # Удаление стоп-слов
    return tokens

df['processed_text'] = df['message'].apply(preprocess_text)

# Создание словаря частотности слов
all_words = [word for tokens in df['processed_text'] for word in tokens]
word_freq = Counter(all_words)

# Пример вывода словаря
print(word_freq.most_common(10))

with open('../data/word_freq.json', 'w', encoding='utf-8') as f:
    json.dump(word_freq, f, ensure_ascii=False, indent=4)