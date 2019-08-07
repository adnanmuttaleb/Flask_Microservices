FROM  python:3.6

WORKDIR /products

COPY . /products

ENV SECRET_KEY dev_products

ENV JWT_SECRET_KEY test

ENV FLASK_APP run.py

RUN pip install -r requirements.txt

EXPOSE "5000"

CMD ["flask", "run"]

