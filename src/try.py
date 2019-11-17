import spacy
from app import find_pop_words
import os

#load language model
nlp = spacy.load('en')

'''
pop_words = find_pop_words()
print("Popular words found:")
print(pop_words)
print("Number of popular words found: " + str(len(pop_words)))

full_content = open('../txt_files/doc1.txt').read()

text_to_process = nlp(full_content)

sentences = list(text_to_process.sents)

print("Total num sentences: " + str(len(sentences)))
#print(sentences)

for word in pop_words:
    hit_sentences = [sent for sent in sentences if word in str(sent)]
    print("Found the following sentences containing popular word " + str(word) +" in the given content:")
    print(hit_sentences)
    print("Number of sentences found: " + str(len(hit_sentences)) + "\n")

#Note the above are inherently associated with specific words

#print("Num sentences with popular words: " + str(len(hit_sentences)))
'''

f_names = []
filepaths = []

file_dir =  '../txt_files/'
for dirname, _, filenames in os.walk(file_dir):
    f_names = filenames
    filepaths = [os.path.join(dirname, filename) for filename in filenames]

#print(filepaths)
filepaths.sort()
f_names.sort()

content_per_doc = {}

for i in range(len(filepaths)):
    filename = f_names[i]
    #print("Filename = " + str(filename))
    #print("Filepath = " + str(filepaths[i]))
    doc = open(filepaths[i])
    plaintext = doc.read().replace('\n', '') # Strip out newline characters common in .txts
        
    #Add content as value to dict with filename as key
    content_per_doc[filename] = plaintext.lower()

#print(content_per_doc)

full_content = ' '.join(content_per_doc.values())
#print(full_content)

word = 'iraq'

hit_docs = {}

#values of hit_docs are lists of documents for which the common word key is a part of the content
hit_docs[word] = [key for key, value in content_per_doc.items() if (word in value)]

print(hit_docs)
