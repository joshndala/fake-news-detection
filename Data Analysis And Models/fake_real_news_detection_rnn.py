# -*- coding: utf-8 -*-
"""fake-real-news-detection_RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TDHehpr8_ON2csnCVrRQU8V7jIpsxTYd

#Library Imports
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import re
from wordcloud import WordCloud #To visualize the text data

from tensorflow.keras.preprocessing.text import Tokenizer #To tokenize the text data
from tensorflow.keras.preprocessing.sequence import pad_sequences #To pad dataset that is not long enough (standardization)
from tensorflow.keras.models import Sequential #Feeding model layers here
from tensorflow.keras.layers import Dense, Embedding, LSTM, Conv1D, MaxPool1D
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

"""#Import Data

##Fake News
"""

fake = pd.read_csv('https://raw.githubusercontent.com/mnkd246/fake-news-detection/main/news_dataset/Fake.csv')

fake.head()

fake.columns

fake['subject'].value_counts()

plt.figure(figsize=(10, 6))
palette = sns.color_palette()
sns.countplot(data=fake, x='subject', palette=palette, hue='subject')

"""**Wordcloud**"""

fake['text'].tolist()

"""From the list, it needs to be merged into a single text data"""

text = ' '.join(fake['text'].tolist()) #The ' ' joins the text data with a space (can be comma, etc)

wordcloud = WordCloud(width=1920, height=1080).generate(text)
fig = plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

"""##Real News"""

real = pd.read_csv('https://raw.githubusercontent.com/mnkd246/fake-news-detection/main/news_dataset/True.csv')

text = ' '.join(real['text'].tolist())

wordcloud = WordCloud(width=1920, height=1080).generate(text)
fig = plt.figure(figsize=(10,10))
plt.imshow(wordcloud)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

"""One notable difference between fake and real news word clouds is the appearance of "Washington Reuters", which is only on real news. Washington Reuters is very well known news service that provides reports from around the world to newpapers and broadcasters.

So unlike the fake news set, real news is more likely to have a source of publication.

Also, some texts are tweets from Twitter. Some texts don't contain any publication information.

#Cleaning Data

First, I will be removing Reuters or Twitter Tweet information from the text
"""

real.sample(5)

unknown_publishers = []
for index, row in enumerate(real.text.values):
  try:
    record = row.split('-', maxsplit=1)
    record[1]

    assert(len(record[0])<120)
  except:
    unknown_publishers.append(index)

len(unknown_publishers)

real.iloc[unknown_publishers].text

real.iloc[8970]

real = real.drop(8970, axis=0)

publisher = []
tmp_text = []

for index, row in enumerate(real.text.values):
  if index in unknown_publishers:
    tmp_text.append(row)
    publisher.append('Unknown')
  else:
    record = row.split('-', maxsplit=1)
    publisher.append(record[0].strip())
    tmp_text.append(record[1].strip())

real['publisher'] = publisher
real['text'] = tmp_text

real.head()

real.shape

"""Fake news rows with empty data:"""

empty_fake_index = [index for index, text in enumerate(fake.text.tolist()) if str(text).strip()==""]

fake.iloc[empty_fake_index]

real['text'] = real['title'] + " " + real['text']
fake['text'] = fake['title'] + " " + fake['text']

real['text'] = real['text'].apply(lambda x: str(x).lower())
fake['text'] = fake['text'].apply(lambda x: str(x).lower())

"""#Preprocessing Text"""

real['class'] = 1
fake['class'] = 0

real.columns

real = real[['text', 'class']]

fake = fake[['text', 'class']]

data = real.append(fake, ignore_index=True)

data.sample(5)

"""Now, we need to remove special characters (colons, etc). This will be done using kgptalkie preprocessing package"""

# Dependencies
!pip install spacy
!python -m spacy download en_core_web_sm
!pip install beautifulsoup4
!pip install textblob
!pip install git+https://github.com/laxmimerit/preprocess_kgptalkie.git --upgrade --force-reinstall

import preprocess_kgptalkie as ps

data['text'] = data['text'].apply(lambda x: ps.remove_special_chars(x))

"""#Vectorization - Word2Vec

The next step is converting the text data to numerical data (aka tokenization)

Word2Vec is one of the most popular techniques to learn word embeddings using shallow neural networks.

Word embedding is the most popular representation of document vocabulary.
"""

import gensim

y = data['class'].values

X = [d.split() for d in data['text'].tolist()]

DIM = 100 #each word will be converted to a sequence of 100 vectors
w2v_model = gensim.models.Word2Vec(sentences = X, vector_size = DIM, min_count = 1)

len(w2v_model.wv.key_to_index)

w2v_model.wv.key_to_index

w2v_model.wv.most_similar('us')

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X)

"""X has now been converted to a set of sequence"""

X = tokenizer.texts_to_sequences(X)

# tokenizer.word_index



"""#Padding"""

plt.hist([len(x) for x in X], bins = 700)
plt.show()

"""Most news have words less than 1000 words, so we can shorten the news with more than 1000 words"""

nos = np.array([len(x) for x in X])
len(nos[nos>1000]) #amount of news that have more than 1000 words

maxlen = 1000
X = pad_sequences(X, maxlen=maxlen)

"""Now the length of ANY index is 1000, even those that had less than 1000 words. This is the padding process

#RNN Modelling
"""

vocab_size = len(tokenizer.word_index) + 1
vocab = tokenizer.word_index

def get_weight_matrix(model):
  weight_matrix = np.zeros((vocab_size, DIM))

  for word, i in vocab.items():
    weight_matrix[i] = model.wv[word]

  return weight_matrix

embedding_vectors = get_weight_matrix(w2v_model)

embedding_vectors.shape

model = Sequential()
model.add(Embedding(vocab_size, output_dim=DIM, weights = [embedding_vectors], input_length=maxlen, trainable=False))
model.add(SimpleRNN(units=128))
model.add(Dense(1, activation='sigmoid')) #since we only have 2 classes
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

model.summary()

X_train, X_test, y_train, y_test = train_test_split(X, y)

model.fit(X_train, y_train, validation_split=0.3, epochs=6)

y_pred = (model.predict(X_test) >= 0.5).astype(int)

accuracy_score(y_test, y_pred)

print(classification_report(y_test, y_pred))

"""#Performing Model on Custom Text Data"""

x = ['Only photo I will tweet. CPR being performed on the soldier now. I heard four shots. #ottawa']
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlen)

(model.predict(x) >= 0.5).astype(int)