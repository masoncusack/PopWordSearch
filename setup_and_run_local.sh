#Install requirements
pip3 install -r requirements.txt

#Move to src
cd ./src

#Download spaCy language model
python3 -m spacy download en

#start app
python3 app.py