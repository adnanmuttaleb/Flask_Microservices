FROM  python:3.6

RUN mkdir /orders

WORKDIR /orders

COPY . /orders/

EXPOSE "5000"

ENV FLASK_RUN_PORT 5000

ENV SECRET_KEY dev_users

ENV JWT_SECRET_KEY test

ENV SQLALCHEMY_DATABASE_URI postgres://postgres:root@localhost:5432/orders_micro

ENV FLASK_RUN_HOST '0.0.0.0'

RUN pip install -r requirements.txt

CMD [ "flask", "run" ]