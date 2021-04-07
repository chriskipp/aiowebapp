FROM python:3.8.2

WORKDIR /usr/src

ADD requirements.txt /usr/src/
ADD requirements-dev.txt /usr/src/

RUN python3 -m pip --no-cache-dir install -U pip && python3 -m pip --no-cache-dir install -r requirements.txt
RUN python3 -m pip --no-cache-dir install -r requirements-dev.txt
RUN sed -i -e '28s/(?m)//' -e "28s/r'/r'(\?m)/"  ../local/lib/python3.8/site-packages/aiohttp_debugtoolbar/tbtools/tbtools.py
RUN sed -i '53s/, loop.*)/)/' /usr/local/lib/python3.8/site-packages/aiohttp/web_server.py

ADD . /usr/src/

CMD ./run.sh
