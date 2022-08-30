FROM python:3.10.5-alpine3.16

WORKDIR /usr/src

ADD requirements.txt /usr/src/
ADD requirements-dev.txt /usr/src/

RUN apk add --update --virtual=buildutils make ca-certificates g++ gcc
RUN apk add --update curl
RUN python3 -m pip --no-cache-dir install -U pip \
  && python3 -m pip --no-cache-dir install -r requirements.txt
RUN python3 -m pip --no-cache-dir install -r requirements-dev.txt
RUN apk del buildutils

#RUN sed -i -e '28s/(?m)//' -e "28s/r'/r'(\?m)/"  ../local/lib/python3.18/site-packages/aiohttp_debugtoolbar/tbtools/tbtools.py
RUN sed -i '53s/, loop.*)/)/' /usr/local/lib/python3.10/site-packages/aiohttp/web_server.py
RUN sed -i '/.decode("utf-8")/d' /usr/local/lib/python3.10/site-packages/aiohttp_session/redis_storage.py

ADD . /usr/src/

CMD ./run.sh
