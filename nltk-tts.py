import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize


# Import the required module for text 
# to speech conversion
from gtts import gTTS

# This module is imported so that we can 
# play the converted audio
import os

# Language in which you want to convert
language = 'en'

#nltk.download()

cadena = "Hello everyone, I am a bot created by Andres Cordova"

text = get_text(cadena)
print("---------------------------------------------")

#Removing square brackets and extra spaces
formatted_article_text = re.sub('[^a-zA-z]', ' ', text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(text)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
     if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#CALCULA LA FRASE QUE MAS SE REPITE
sentence_scores = {}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 30:
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#REALIZA EL RESUMEN CON LAS MEJORES FRASES
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

#IMPRIME EL RESUMEN
print(summary)

myobj = gTTS(text=summary, lang=language, slow=False)
myobj.save("summary.mp3")

# Playing the converted file
os.system("summary.mp3")


print("---------------------------------------------")