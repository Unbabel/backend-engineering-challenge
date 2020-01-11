FROM python:3.8

RUN mkdir /app

ADD . /app

WORKDIR /app

RUN make test

RUN make install

RUN enki -h
