FROM python:3.7

WORKDIR /usr/src/app
RUN pip3 install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime
COPY main.py imdb-head.vocab imdb.vocab text_classification_v2.tflite  ./
ENTRYPOINT ["python", "main.py" ]