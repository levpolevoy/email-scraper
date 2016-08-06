from scrapy import Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
from scrapy_splash import SplashRequest
from commonregex import CommonRegex

common_regex_parser = CommonRegex()


class DuplicatesPipeline(object):
    def __init__(self):
        self.seen = set()

    def process_item(self, item, spider):
        if 'email' not in item:
            raise DropItem("Invalid item: %s. Must contain an email." % item)
        if item['email'] in self.seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.seen.add(item['email'])
            return item


class EmailAddressesSpider(Spider):
    name = 'email-addresses-spider'
    custom_settings = {
        'DEPTH_LIMIT': 1,
        # Ignore files larger than 100KB. They are unlikely to be HTML file.
        'DOWNLOAD_MAXSIZE': 100 * 1024,
        'ITEM_PIPELINES': {'find_emails.DuplicatesPipeline': 1},

        # --------------------------------------------------------
        # Settings that are related to integration with "splash".
        # We use "splash" to execute JavaScript on HTML pages.
        #
        # See more info here: https://github.com/scrapy-plugins/scrapy-splash
        #
        'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_splash.SplashCookiesMiddleware': 723,
            'scrapy_splash.SplashMiddleware': 725,
            'scrapy.downloadermiddlewares.httpcompression.'
            'HttpCompressionMiddleware': 810,
        },
        'SPIDER_MIDDLEWARES': {
            'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
        },
        'SPLASH_URL': 'http://localhost:8050'
        # --------------------------------------------------------
    }

    def __init__(self, domain=None):
        super(Spider, self).__init__()
        if not domain:
            raise ValueError('Must pass a domain')

        self.domain = domain

    @property
    def allowed_domains(self):
        # In some cases a domain may be passed with a port.
        # Example: "localhost:8000".
        #
        # The latter is technically not a domain. Only "localhost" is the
        # domain, and it is important to set it correctly in
        # "allowed_domains", otherwise the crawler will skip on pages
        # that it should not skip on.
        domain_without_optional_port = self.domain.split(':')[0]
        return [domain_without_optional_port]

    def start_requests(self):
        return [SplashRequest('http://%s' % self.domain)]

    def parse(self, response):
        # Extract emails from the page text using a regex match
        for email in common_regex_parser.emails(response.text):
            yield {'email': email}

        # Find new links to crawl
        for lnk in LinkExtractor().extract_links(response):
            yield SplashRequest(lnk.url)
