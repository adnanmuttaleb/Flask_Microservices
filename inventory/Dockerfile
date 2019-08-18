FROM  python:3.6

WORKDIR /inventory

COPY . /inventory

ENV SECRET_KEY dev_inventory

ENV JWT_SECRET_KEY test

ENV FLASK_APP run.py

ENV FLASK_RUN_PORT 5000

ENV FLASK_RUN_HOST '0.0.0.0'

RUN pip install -r requirements.txt

EXPOSE "5000"

CMD [ "flask", "run" ]


