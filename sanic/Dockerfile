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

COPY . .

CMD ["python3", "-m", "app"]
#CMD ["python3", "-m", "pip", "list"]
