FROM python:3.10.5-alpine3.16

WORKDIR /usr/src

COPY requirements.txt /usr/src/
COPY requirements-dev.txt /usr/src/

#=============================================
# This is a Bugfix for failing build of pyaml
# since cython==3
# /!\ Review soon!
RUN echo "cython<3" > constraint.txt
ENV PIP_CONSTRAINT constraint.txt
#=============================================

RUN apk add --update --virtual=buildutils make ca-certificates g++ gcc \
  && apk add --update curl \
  && python3 -m pip --no-cache-dir install -U pip \
  && python3 -m pip --no-cache-dir install -r requirements.txt \
  && python3 -m pip --no-cache-dir install -r requirements-dev.txt \
  && apk del buildutils

#=============================================
RUN rm constraint.txt
#=============================================

RUN sed -i '/.decode("utf-8")/d' /usr/local/lib/python3.10/site-packages/aiohttp_session/redis_storage.py
RUN sed -i -e '28s/(?m)//' -e "28s/r'/r'(\?m)/"  ../local/lib/python3.10/site-packages/aiohttp_debugtoolbar/tbtools/tbtools.py
RUN sed -i '53s/, loop.*)/)/' /usr/local/lib/python3.10/site-packages/aiohttp/web_server.py

COPY . /usr/src/

CMD ["python3", "-m", "app", "-c", "config/dev.yaml"]
