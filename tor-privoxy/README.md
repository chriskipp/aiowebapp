# Tor-Privoxy-Docker

Provides an zero set up and instantly availible
entry point to the tor netword that is reachable
over http/https as well as via socks5 protocoll.

## Startup

```bash
docker-compose --build up tor-privoxy
```

## Testing the Connection

```bash
# No tor
curl 'http://httpbin.org/ip'

# tor via http
curl --proxy "http://localhost:8888" \
  'http://httpbin.org/ip'
 
# tor via socks
curl --proxy "socks5://localhost:9050" \
  'http://httpbin.org/ip'

# Output should look similar to this:
# {
#   "origin": "91.14.106.95"
# }
# {
#   "origin": "45.61.186.108"
# }
# {
#   "origin": "45.61.186.108"
# }
```

