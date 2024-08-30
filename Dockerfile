FROM python:3.12

ADD main.py restaurants.csv tests.py ./

RUN pip install fastapi uvicorn
