from scrapy import Spider, Request
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import DropItem
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
        'ITEM_PIPELINES': {'find_emails.DuplicatesPipeline': 1}
    }

    def __init__(self, domain=None):
        if not domain:
            raise ValueError('Must pass a domain')

        self.start_urls = ['http://%s' % domain]

        # In some cases a domain may be passed with a port.
        # Example: "localhost:8000".
        #
        # The latter is technically not a domain. Only "localhost" is the
        # domain, and it is important to set it correctly in
        # "allowed_domains", otherwise the crawler will skip on pages
        # that it should not skip on.
        domain_without_optional_port = domain.split(':')[0]
        self.allowed_domains = [domain_without_optional_port]

    def parse(self, response):
        # Extract emails from the page text using a regex match
        for email in common_regex_parser.emails(response.text):
            yield {'email': email}

        # Find new links to crawl
        for lnk in LinkExtractor().extract_links(response):
            yield Request(lnk.url)
