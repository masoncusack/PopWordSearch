import spacy
from collections import Counter
import json
import zipfile
from flask import Flask, request, Response, flash, redirect, render_template
from werkzeug.utils import secure_filename
import os

#TODO: How do we want to handle keeping track of sentences? Go back in and retrieve them or can we track them from the beginning?
#I think we'll need to go back and re-process if we need all sentences where the common words occur.
#TODO: best way to output as table?
#TODO: write tests and consider CI/CD. In fact, consider deploying this as a site/API
#TODO: setup.sh bash script that does e.g. python3 -m spacy download en (or whatever it was)
#TODO: consider support for Mandarin Chinese or another language?

# Set host and port
ADDRESS = '0.0.0.0'
PORT = 8000

#Path to upload folder
UPLOAD_FOLDER = '../test_docs'

# Restrict extensions
ALLOWED_EXTENSIONS = {'zip'}  # restrict to .zip upload for now
# ALLOWED_EXTENSIONS = {'txt', 'jpg', 'png'} #Can always extend to other filetypes later

# Initialize app:
app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def handle_file_upload():
    if request.method == 'POST':

        if 'zip' not in request.files:
            flash('No file uploaded/found')
            return redirect(request.url)
        #else
        files = request.files['zip']
        if files.filename =='':
            flash('Filename missing')
            return redirect(request.url)
        if files and allowed_file(files.filename): #check that is not None
            filename = secure_filename(files.filename)
            print("\nUploaded filename: " + str(filename))
            #TODO: safe zip file locally for to test_docs for analysis
            files.save(os.path.join(UPLOAD_FOLDER, filename))
            #TODO: unzip all contained files to get txts
            #TODO: delete all files in test_docs once the result is returned

    return render_template('index.html')

#Open test doc 1
doc = open('../test_docs/doc1.txt')
plaintext = doc.read().replace('\n', '') #strip out newline characters common in .txts

#How many top common words would you like to find?
num_common_words = 10

#Load English language model
nlp = spacy.load('en')

doc = nlp(plaintext) #Take out new lines

#Find words/"tokens", removing stop words
words = [token.text for token in doc if token.is_punct != True and token.is_stop != True]

#Find the n most common words
num_words = Counter(words)
common_words = num_words.most_common(num_common_words)

print(common_words)

#Convert to json for response (can be rendered in table on front end)
#TODO: the below needs to be generated for each popular word
def gen_response():
    response_data_entry = {
        "Word(#)": {

        },
        "Documents": {
            
        },
        "Sentences containing the word": {

        }
    }
    
    response_string = json.dumps(response_data_entry)    
    print(response_string)
    
    return response_string

if __name__ == '__main__':
    app.run(host=ADDRESS, port=PORT) #Run over http for sake of ease (not secure for production)