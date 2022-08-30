FROM python:3.10.5-alpine3.16

COPY . /srv
WORKDIR /srv

RUN apk add --update --virtual=buildutils make ca-certificates g++ gcc
RUN python3 -m pip --no-cache-dir install -r requirements.txt
RUN apk del buildutils

#CMD ["python3", "simple_async_view.py"]
CMD ["python3", "websocket.py"]
