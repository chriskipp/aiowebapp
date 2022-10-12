FROM python:3.9

WORKDIR /usr/src

ADD . /usr/src/

RUN python3 -m pip install -U pip && python3 -m pip install -r requirements.txt

CMD ["scrapy", "crawl", "redisspider"]
