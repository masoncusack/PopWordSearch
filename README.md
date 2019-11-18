# PopWordSearch
Simple flask-based NLP service utilising spaCy to find the most popular words within texts and retrieve the sentences they originate from.

## General

This is a Flask app serving a basic HTML frontend which allows you to upload a .zip like the one provided, analyses the content of text files therein, and returns the most common words, the documents they appear in, and a selection of sentences within those documents where the words appear. 

The HTML form allows you to change the number of common words you look for. I.e. the 10 most common versus the 5 most common, and also how many example sentences to return, which

## The approach

Parameterised HTML was used due to the lack of time to build a proper front end. I do not class myself as proficient in front end development, and would be happy to discuss the many better ideas for a production scenario.

## In the future...

I'd like to:

- Do more error handling
- Write unittests which report out to the CI/CD process in GitHub/Azure Devops


## Running the app

### Prerequisites

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