# PopWordSearch
Simple flask-based NLP service utilising [spaCy](https://spacy.io) to find the most popular words within texts and retrieve the sentences they originate from.

## General

This is a Flask app serving a basic HTML frontend which allows you to upload a .zip like the one provided, analyses the content of text files therein, and returns the most common words, the documents they appear in, and a selection of sentences within those documents where the words appear. 

The HTML form allows you to change the number of common words you look for. I.e. the 10 most common versus the 5 most common, and also how many example sentences to return, which

## The approach

We use spaCy's English language model to produce 3 functionalities:
- Finding common words across documents, by tokenizing text and removing stop words such as 'and', 'the', etc., in order to produce more valuable results (`find_pop_words`)
- Finding all documents in which each of these common words appears, maintaining a dictionary of words-to-filenames (`find_documents`)
- Finding all sentences in which each common word appears, maintaining a dictionary of words-to-sentences (`find_sentences`)

The user can choose how many common words to find, and how many example sentences the app should return for each.

This could easily be expanded to support documents in German, French, Greek, and more languages, by utilising [spaCy's other language models](https://spacy.io/usage/models), and language detection.

Parameterised HTML was used as a makeshift frontend due to the lack of time to build out a more elaborate one. I do not class myself as proficient in front end development, and would be happy to discuss the many better ideas for a production scenario. I would suggest the production of a suitable front end constitutes another project.

## In the future...

I'd like to:

- Do more error handling - the current form of the app can easily be broken by, for example, failing to upload a .zip. A mature frontend can better model dynamic state, to reject certain inputs and give warnings in a way that doesn't lead to failures, and instructs users.
- Write unittests which report out to the CI/CD process in GitHub/Azure Devops
- Exploring other data structures and approaches for processing text to make this faster and more memory efficient, particularly as the number of files increases
- As part of additional front-end work, explore better ways of visualising the returned data, large numbers of sentence examples in particular are difficult to display neatly and readably in a table structure.

## Running the app

### Prerequisites

- git (if wanting to clone)
- Python 3 installed (3.7+)
- python3-pip (pip3 package manager)

### Optional/useful

- Docker

### If wanting to run locally

In this case it may be sensible to set up a virtualenv to avoid installing required packages globally on your local system.

Setup can be done as follows:

1. Install requirements

```bash
#Navigate into repo root
cd popwordsearch
#Install all requirements
pip3 install -r requirements.txt
#Download spaCy English language model
python3 -m spacy download en
```

2. Run app

```bash
cd src
python3 app.py
```

You can then use the app by going to [localhost:8000](http://localhost:8000) in your browser.

You also have the choice of running `setup_and_run_local.sh` in a bash shell, which will do setup and start the app for you running on localhost. This can be done as follows:

```bash
#Navigate into repo root
cd popwordsearch
#Give execute permission to script
chmod +x setup_and_run_local.sh
#Set up and run app
./setup_and_run_local.sh
```

You can then use the app by going to [localhost:8000](http://localhost:8000) in your browser.

### If wanting to use Docker 

If you have Docker installed, the Dockerfile in the repo root will allow you to build a lightweight, deployment-ready Python image with all requirements installed. 

This can be used as follows:

1. Build Docker image

```bash
cd popwordsearch

#Build and tag
docker build -t popwordsearch:demo .
```

2. Run docker image

```bash
docker run -t -p 8000:8000 popwordsearch:demo
```


You can then use the app by going to [localhost:8000](http://localhost:8000) in your browser.