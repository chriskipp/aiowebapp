FROM python:3.8.2

WORKDIR /usr/src

ADD . /usr/src/

RUN pip install -U pip && pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

CMD ./run.sh
