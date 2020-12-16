FROM redislabs/redisearch:2.0.2

COPY redis.conf /usr/local/etc/redis/redis.conf
COPY modules /usr/lib/redis/modules

CMD [ "redis-server", "/usr/local/etc/redis/redis.conf" ]
