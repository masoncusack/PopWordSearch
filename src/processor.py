import spacy
from collections import Counter
import re #regex

#TODO: take out new lines '\n'

#Open test doc 1
doc = open('../test_docs/doc1.txt')

#How many top common words would you like to find?
num_common_words = 10

nlp = spacy.load('en')

doc = nlp(doc.read())

#Find words/"tokens", removing stop words
words = [token.text for token in doc if token.is_punct != True and token.is_stop != True]

#Find the n most common words
num_words = Counter(words)
common_words = num_words.most_common(num_common_words)

print(common_words)