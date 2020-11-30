FROM python:3.8.2

WORKDIR /usr/src

ADD requirements.txt /usr/src/
ADD requirements-dev.txt /usr/src/

RUN pip install -U pip && pip install -r requirements.txt
RUN pip install -r requirements-dev.txt

ADD . /usr/src/

CMD ./run.sh
