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

# Initialize app
app = Flask(__name__)

# Load spaCy's English language model
nlp = spacy.load('en')

def create_dir(path):
    #refresh
    if os.path.isdir(path):
        shutil.rmtree(path)
    
    os.mkdir(path)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def unzip(zip_name, in_path, out_path='../txt_files/'): #Note: if out_path changes, so will file_dir in find_pop_words()
    zip_ref = zipfile.ZipFile(in_path, 'r')
    create_dir(out_path)
    zip_ref.extractall(out_path)
    zip_ref.close()
    
    #Remove containing folder & copy files to generic txt directory for processing
    source_dir = out_path+zip_name.rsplit('.', 1)[0]+'/'
    file_list = os.listdir(source_dir)
    file_paths = [source_dir+filename for filename in file_list]
    for f in file_paths:
        shutil.copy2(f, out_path)
    
    #Cleanup
    shutil.rmtree(UPLOAD_FOLDER)
    shutil.rmtree(source_dir)

def find_pop_words(num_common_words=10, file_dir="../txt_files"): #by default search for 10 most common

    #Get filepaths of uploaded txts
    filepaths = []
    
    for dirname, _, filenames in os.walk(file_dir):
        for filename in filenames:
            filepaths.append(os.path.join(dirname, filename))

    # Sort filepaths because for some reason os.walk paths are unordered.
    filepaths.sort()

    # Maintain ordered list to associate text bodies with specific files
    content_per_doc = []

    # Concat all content to find popular words
    full_content = ""

    for f in filepaths:
        doc = open(f)
        plaintext = doc.read().replace('\n', '') # Strip out newline characters common in .txts
        content_per_doc.append(plaintext)
        full_content += plaintext+" " # Add spaces to ensure tokens are recognised correctly (spaCy may handle this anyway)

    # Process to find common words across documents
    text_to_process = nlp(full_content)

    # Find words/"tokens", removing stop words
    words = [token.text for token in text_to_process if token.is_punct != True and token.is_stop != True]

    # Find the n most common words
    num_words = Counter(words)
    common_words = num_words.most_common(num_common_words)

    #TODO: return results and use in other processing functions, then wrap
    #Return words only, not their count, as we don't need this in any results
    return [word[0] for word in common_words]

#TODO: find which documents each popular word appears in
def which_documents(content_per_doc, word):
    return render_template('index.html')

#TODO: find sentences in which each popular word appears
def find_sentences(full_content, word):
    return render_template('index.html')

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

            #Ensure there is an uploads folder
            create_dir(UPLOAD_FOLDER)
            
            #Save files locally for processing
            files.save(os.path.join(UPLOAD_FOLDER, zipname))
            
            #Unzip all contained files to get txts
            unzip(zip_name=zipname, in_path=UPLOAD_FOLDER+zipname) #out_path has default

            #If the user submits a specific number of common words they want
            if request.form['num_common_words'] is not None:
                num_common_words = request.form['num_common_words']
                common_words = find_pop_words(num_common_words=int(num_common_words))
            else:
                common_words = find_pop_words() #use default
            
            print("Common words: " + str(common_words))

    return render_template('index.html')

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
    #print(response_string)
    
    return response_string

if __name__ == '__main__':
    app.run(host=ADDRESS, port=PORT) #Run over http for sake of ease (not secure for production)