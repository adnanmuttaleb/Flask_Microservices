FROM  python:3.6

COPY requirements.txt /auth/requirements.txt

WORKDIR /auth

RUN pip install -r requirements.txt

COPY . /auth

ENV SECRET_KEY dev_auth

ENV JWT_SECRET_KEY test

ENV FLASK_APP run.py

ENV FLASK_RUN_PORT 5000

ENV FLASK_RUN_HOST '0.0.0.0'
 
EXPOSE "5000"

CMD flask db upgrade && flask run