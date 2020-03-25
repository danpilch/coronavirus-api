FROM python:3.8.2-buster

COPY ./api.py ./requirements.txt /

RUN pip install -r requirements.txt

CMD [ "python", "-u", "./api.py" ]
