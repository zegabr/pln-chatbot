FROM python:3.8.8-slim

COPY . /src

WORKDIR /src

RUN pip3 install -U pip
RUN pip install rasa
RUN pip install -r requirements.txt
RUN rasa train

CMD ["rasa", "run"]
