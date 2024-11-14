FROM python:3.9-slim

RUN pip install --upgrade pip 
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY online_inference.py /online_inference.py

ENTRYPOINT [ "fastapi", "run", "/online_inference.py", "--port", "80"]