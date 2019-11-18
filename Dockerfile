FROM python:3.7

RUN apt-get update

ADD requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r /app/requirements.txt

#Install spaCy language model
RUN python3 -m spacy download en

ADD src /app/src
WORKDIR /app/src

EXPOSE 8000
CMD python3 app.py