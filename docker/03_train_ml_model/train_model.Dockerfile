FROM python:3.9-slim

RUN pip install --upgrade pip 
RUN apt -y update && apt -y install git
RUN git clone https://github.com/misis-mlops2024/base.git 

WORKDIR /base
RUN pip install --upgrade pip 
RUN python setup.py install
RUN pip install -r requirements.txt

ENTRYPOINT [ "dvc", "repro" ]