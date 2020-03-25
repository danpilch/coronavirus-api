FROM python:3.8.2-buster

COPY ./data.py ./requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./data.py" ]
