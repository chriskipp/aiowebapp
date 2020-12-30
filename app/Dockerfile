FROM python:3.8.2

WORKDIR /usr/src

ADD requirements.txt /usr/src/
ADD requirements-dev.txt /usr/src/

RUN pip --no-cache-dir install -U pip && pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install -r requirements-dev.txt
RUN sed -i -e '28s/(?m)//' -e "28s/r'/r'(\?m)/"  ../local/lib/python3.8/site-packages/aiohttp_debugtoolbar/tbtools/tbtools.py

ADD . /usr/src/

CMD ./run.sh
