import spacy
from collections import Counter
import json
import zipfile
from flask import Flask, request, Response, flash, redirect, render_template
from werkzeug.utils import secure_filename
import shutil, os

#TODO: setup.sh bash script that does e.g. python3 -m spacy download en (or whatever it was)
#TODO: consider support for Mandarin Chinese or another language? (should be transferable)

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

#Find the most common words across all documents
def find_pop_words(num_common_words=10, file_dir="../txt_files"): #by default search for 10 most common

    #Get filepaths of uploaded txts
    filepaths = []
    f_names = []
    
    for dirname, _, filenames in os.walk(file_dir):
        f_names = filenames
        filepaths = [os.path.join(dirname, filename) for filename in filenames]

    # Sort filepaths because for some reason os.walk paths are unordered.
    filepaths.sort()
    f_names.sort()

    # Dict to associating text body to each individual file
    content_per_doc = {}

    for i in range(len(filepaths)):
        filename = f_names[i]
        #print("Filename = " + str(filename))
        #print("Filepath = " + str(filepaths[i]))
        doc = open(filepaths[i])
        plaintext = doc.read().replace('\n', '').lower() # Strip out newline characters common in .txts and turn to lowercase to avoid token duplication
        
        #Add content as value to dict with filename as key
        content_per_doc[filename] = plaintext
        

    # Concat all content to find popular words across documents
    full_content = ' '.join(content_per_doc.values())

    # Process to find common words across documents
    text_to_process = nlp(full_content)

    # Find words/"tokens", removing stop words
    words = [str(token.text) for token in text_to_process if token.is_punct != True and token.is_stop != True]

    # Find the n most common words
    num_words = Counter(words)
    common_words = num_words.most_common(num_common_words)

    #TODO: return results and use in other processing functions, then wrap
    #Return words only, not their count, as we don't need this in any results
    return [str(word[0]) for word in common_words], content_per_doc, full_content

# Find which documents each popular word appears in
def find_documents(content_per_doc, pop_words):
    hit_docs = {}
    for word in pop_words:
        #values of hit_docs are lists of documents for which the common word key is a part of the content
        hit_docs[word] = [str(key) for key, value in content_per_doc.items() if (word in value)]
    return hit_docs

# Find which sentences a popular word appears in across all documents.
def find_sentences(full_content, pop_words):

    text_to_process = nlp(full_content) #TODO: should we do this globally?

    sentences = list(text_to_process.sents)

    hit_sentences = {}

    #Associate sentences with their contained popular words
    for word in pop_words:
        hit_sentences[str(word).lower()] = [str(sent) for sent in sentences if word in str(sent)] #Values are lists of sentences that associated word is in

    return hit_sentences

@app.route("/", methods=['GET', 'POST'])
def handle_file_upload():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':

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

            #TODO: build response for front end
            
            #1. Get common words across documents
            
            #If the user submits a specific number of common words they want
            #TODO: protect against the case when num_common_words is negative
            if request.form['num_common_words'] is not None:
                num_common_words = request.form['num_common_words']
                common_words, content_per_doc, full_content = find_pop_words(num_common_words=int(num_common_words))
            else:
                common_words, content_per_doc, full_content = find_pop_words() #use default

            #Number of sentence examples to return according to form
            num_sentences = request.form['num_sentences']

            #2. Get the documents in which each word appears
            
            hit_docs = find_documents(content_per_doc, common_words)

            #3. Get the sentences in which each word appears

            hit_sentences = find_sentences(full_content, common_words)

            #4. Return and render results

            #Example result entry
            print("Common word: ")
            sought_word = common_words[1]
            print(sought_word)
            
            print("\nDocuments where this word appears: ")
            print(hit_docs[sought_word])

            print("\nSentences where this word appears: ")
            print(hit_sentences[sought_word])
            
            #Render results
            result_table = gen_result_table(common_words, hit_docs, hit_sentences, num_sentences)
            return param_html(result_table)

#Parameterise html to display results because I don't have time to build a front end
def param_html(result_table):
    return('<!DOCTYPE html>'+
            '<html style="zoom:200%; max-width:500px; margin:auto">'
            '<head>'+
                '<meta charset="UTF-8">'+
                '<title>Natural language analysis</title>'+
            '</head>'+
            '<body style="text-align:center">'+
                '<h1 style="text-align:center">Upload a .zip folder of .txt files for analysis</h1>'+
                '<br>'+
                    '<form method="post" action="/" enctype="multipart/form-data">'+
                        '<input type="file" name="zip" id="zip">'+
                        '<br/><br/>'+
                        '<label for="lfname">Number of common words to find:</label>'+
                        '<input type=number name="num_common_words" id="num_common_words" value="10">'+
                        '<br/><br/>'+
                        '<label for="num_sentences">Number of sentence examples to return:</label>'+
                        '<input type=number name="num_sentences" id="num_sentences" value="3">'+
                        '<br/><br/>'+
                        '<input type="submit" value="Upload"></form>'+
                        '<br/><br/><hr/>'+
                    '</form>'+
                '<h3 style="color:black">Results: </h3>'+
                        result_table+
                '</h3>'+
            '</body>'+
            '</html>')


#Convert result to json for response (can be rendered in table on front end)
#TODO: the below needs to be generated for each popular word
def gen_result_table(common_words, hit_docs, hit_sentences, num_sentences):
    
    entries = '' #Initially no classifications

    for word in common_words:
        entries+=('<tr>'+
                    '<td>'+word+'</td>'+
                    '<td>'+', '.join(hit_docs[word])+'</td>'+
                    '<td>'+'<br/> '.join(hit_sentences[word][:int(num_sentences)])+'</td>'+
                '</tr>')
        #New row for each common word

    table = ('<table style="margin-right:auto; margin-left:auto; width:400px;" border="1">'+
                '<tr>'+
                    '<th>Word(#)</th>'+
                    '<th>Documents containing this word</th>'+
                    '<th>Some sentences containing this word</th>'+
                '</tr>'+entries+
            '</table>') #If somehow no results, will just render empty table
            
    return table

if __name__ == '__main__':
    app.run(host=ADDRESS, port=PORT) #Run over http for sake of ease (not secure for production)