FROM  python:3.6

COPY requirements.txt /inventory/requirements.txt

WORKDIR /inventory

RUN pip install -r requirements.txt

COPY . /inventory

ENV SECRET_KEY dev_inventory

ENV JWT_SECRET_KEY test

ENV FLASK_APP run.py

ENV FLASK_RUN_PORT 5000

ENV FLASK_RUN_HOST '0.0.0.0'

EXPOSE "5000"

CMD [ "flask", "run"]