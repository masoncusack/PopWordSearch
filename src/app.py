import spacy
from collections import Counter
import json
import zipfile
from flask import Flask, request, Response, flash, redirect, render_template
from werkzeug.utils import secure_filename
import shutil, os

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
UPLOAD_FOLDER = '../uploads/'

# Restrict extensions
ALLOWED_EXTENSIONS = {'zip'}  # restrict to .zip upload for now
# ALLOWED_EXTENSIONS = {'txt', 'jpg', 'png'} #Can always extend to other filetypes later

# Initialize app:
app = Flask(__name__)

def create_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)

create_dir(UPLOAD_FOLDER)

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
            zipname = secure_filename(files.filename)
            print("\nUploaded filename: " + str(zipname))
            #Save files locally for processing
            files.save(os.path.join(UPLOAD_FOLDER, zipname))
            #Unzip all contained files to get txts
            zip_ref = zipfile.ZipFile(UPLOAD_FOLDER+zipname, 'r')
            outpath = '../txt_files/' #txts in here
            create_dir(outpath)
            zip_ref.extractall(outpath)
            zip_ref.close()
            #Remove containing folder & copy files to generic txt directory for processing
            source_dir = outpath+zipname.rsplit('.', 1)[0]+'/'
            file_list = os.listdir(source_dir)
            file_paths = [source_dir+filename for filename in file_list]
            for f in file_paths:
                shutil.copy2(f, outpath)
            #TODO: Cleanup
            shutil.rmtree(UPLOAD_FOLDER)
            shutil.rmtree(source_dir)

    return render_template('index.html')

''' TODO: process docs as below to find the most popular words
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
'''

#Convert result to json for response (can be rendered in table on front end)
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