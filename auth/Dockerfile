FROM  python:3.6

WORKDIR /auth

COPY . /auth

ENV SECRET_KEY dev_auth

ENV JWT_SECRET_KEY test

ENV FLASK_APP run.py

RUN pip install -r requirements.txt

RUN flask db init

RUN flask db migrate

RUN flask db upgrade

EXPOSE "5001"

CMD ["flask", "run"]

