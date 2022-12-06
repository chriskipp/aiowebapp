FROM python:3.10.5-alpine3.16

WORKDIR /src

COPY requirements.txt requirements.txt

RUN apk add \
  --update \
  --virtual=buildutils \
  make \
  ca-certificates\
  g++ \
  gcc \
  && python3 -m pip --no-cache-dir install -U pip \
  && python3 -m pip --no-cache-dir install -r requirements.txt \
  && rm requirements.txt \
  && apk del buildutils

RUN sed -i -e 's/app\.extensions/app.ctx.extensions/g' -e 's/app, ex/app.ctx, ex/g' /usr/local/lib/python3.10/site-packages/sanic_dropzone/*.py
COPY . .

WORKDIR /src/app

CMD ["sanic", "--fast", "--dev", "--access-logs", "server:app", "--host=0.0.0.0"]
#CMD ["python3", "-m", "pip", "list"]
