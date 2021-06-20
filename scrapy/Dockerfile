FROM python:3.9

RUN python3 -m pip install -U pip && python3 -m pip install -r requirements.txt

ENTRYPOINT ["scrapy"]
CMD ["crawl", "dmoz"]
