import spacy
from collections import Counter

#TODO: Do we want to process all documents or one by one? Surely all together become less instructive.
#TODO: How do we want to handle keeping track of sentences? Go back in and retrieve them or can we track them from the beginning?
#I think we'll need to go back and re-process if we need all sentences where the common words occur.
#TODO: best way to output as table?
#TODO: write tests and consider CI/CD. In fact, consider deploying this as a site/API

#Open test doc 1
doc = open('../test_docs/doc1.txt')
plaintext = doc.read().replace('\n', '') #strip out newline characters common in .txts

#How many top common words would you like to find?
num_common_words = 10

nlp = spacy.load('en')

doc = nlp(plaintext) #Take out new lines

#Find words/"tokens", removing stop words
words = [token.text for token in doc if token.is_punct != True and token.is_stop != True]

#Find the n most common words
num_words = Counter(words)
common_words = num_words.most_common(num_common_words)

print(common_words)