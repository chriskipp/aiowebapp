#FROM python:3.10.5-alpine3.16
FROM python:3.10.5

WORKDIR /usr/scheduler

RUN apt-get update && \
  apt-get install --yes --no-install-recommends libsasl2-dev libldap2-dev libssl-dev python3-dev

RUN python3 -m pip --no-cache-dir install -U pip wheel

RUN git clone "https://github.com/chriskipp/ndscheduler" \
  && cd ndscheduler \
  && sed -i 's/ndscheduler-fork/ndscheduler/g' setup.py \
  && python3 -m pip install . \
  && cd -\
  && rm -rf ndscheduler
RUN git clone "https://github.com/chriskipp/simple_scheduler" \
  && cd simple_scheduler \
  && python3 setup.py install \
  && cd - \
  && rm -rf simple_scheduler
RUN python3 -m pip --no-cache-dir install construct python-ldap
RUN git clone "https://github.com/djacobs/PyAPNs.git" \
  && cd PyAPNs && python3 setup.py install \
  && cd -

WORKDIR /src/scheduler
COPY ./config.yaml .

COPY ./.pgpass /root/
RUN chmod 0600 /root/.pgpass

ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/src/scheduler/scripts/bin
EXPOSE 7777

CMD ["/usr/local/bin/simple_scheduler", "-y", "config.yaml"]
