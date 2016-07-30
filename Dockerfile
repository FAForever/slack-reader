FROM python:3.5.2-alpine

ADD . /src

WORKDIR /src

RUN pip install -r requirements.txt

CMD [ "python", "./app.py"]
