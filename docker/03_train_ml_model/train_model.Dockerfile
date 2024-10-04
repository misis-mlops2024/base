FROM python:3.9-slim

RUN pip install --upgrade pip 
RUN git clone git clone https://github.com/misis-mlops2024/base.git 

WORKDIR /base


ENTRYPOINT [ "dvc", "repro" ]