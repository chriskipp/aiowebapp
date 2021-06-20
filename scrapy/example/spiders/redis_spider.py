from urllib.parse import urljoin
from scrapy_redis.spiders import RedisSpider
import scrapy


class MySpider(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    #name = "crawldomain"
    name = 'redisspider'
    redis_key = 'redisspider:start_urls'

    #custom_settings = {
    #    'COOKIES_ENABLED': True,
    #    'RETRY_ENABLED': True,
    #    'DOWNLOAD_TIMEOUT': 60,
    #    'REDIRECT_ENABLED': True,
    #    'AJAXCRAWL_ENABLED': True,
    #    'DOWNLOAD_MAXSIZE': 2097152,
    #    'ROBOTSTXT_OBEY': False
    #}

    def __init__(self, domain=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [domain]
        self.allowed_domains = [domain]

    def start_requests(self):
        for url in self.start_urls:
            if url:
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #for href in response.xpath('//a/@href').getall():
        #    self.log(href)
        #    url = urljoin(response.url, href)
        #    yield scrapy.Request(url, callback=self.parse)

        endpoint_item = {
            'status': response.status,
            'url': response.url,
            'mimetype': response.headers[b'Content-Type'].decode(),
            'size': (b'Content-Length' in response.headers
                        and response.headers[b'Content-Length'].decode()
                        or None
                    )
        }

        if endpoint_item['mimetype'] == 'text/html':
            endpoint_item['title'] = response.xpath('//title/text()').get()
            if endpoint_item['title']:
                endpoint_item['title'] = endpoint_item['title'].strip()

        yield endpoint_item

        for href in response.xpath('//a/@href').getall():
            url = urljoin(response.url, href)
            link_item = {
                    'type': 'link',
                    'source': response.url,
                    'dest': url
            }
            yield link_item

            #if url.find('?') == -1:
            if True:
                if url.startswith('mailto:'):
                    yield {
                            'url': response.url,
                            'email': url
                          }
