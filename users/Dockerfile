FROM  python:3.6

WORKDIR /project

COPY . /project/users

RUN pip install -r users/requirements.txt

ENV SECRET_KEY dev

ENV FLASK_APP users

ENV FLASK_RUN_PORT "5000"

ENV FLASK_RUN_HOST "0.0.0.0"

EXPOSE "5000"

CMD ["flask", "run"]

