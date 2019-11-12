import spacy
from collections import Counter

#TODO: take out stop words so we don't capture "the"
#How many top common words would you like to find?
num_common_words = 1

nlp = spacy.load('en')

doc = nlp(u'Hello there, how are you? Hello hello hello')

#Find words/"tokens"
words = [token.text for token in doc if token.is_punct != True]

#Find the n most common words
num_words = Counter(words)
common_words = num_words.most_common(num_common_words)

print(common_words)