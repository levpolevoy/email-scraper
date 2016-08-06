import unittest
from find_emails import DuplicatesPipeline, EmailAddressesSpider
from scrapy.exceptions import DropItem
from scrapy.http import TextResponse
from scrapy_splash import SplashRequest


class TestDuplicatesPipeline(unittest.TestCase):
    def setUp(self):
        self.d = DuplicatesPipeline()
        self.item = {'email': 'abc'}

    def test_should_not_skip_on_item_seen_for_the_first_time(self):
        self.d.process_item(self.item, None)
        self.assertIn(self.item['email'], self.d.seen)

    def test_should_skip_on_items_that_were_seen_before(self):
        self.d.process_item(self.item, None)
        self.assertRaises(DropItem,
                          lambda: self.d.process_item(self.item, None))

    def test_should_skip_on_items_without_an_email_address(self):
        bad_item = {'this_is_not': 'an email address'}
        self.assertRaises(DropItem,
                          lambda: self.d.process_item(bad_item, None))


class TestEmailAddressesSpider(unittest.TestCase):
    def test_must_set_a_domain(self):
        self.assertRaises(ValueError, EmailAddressesSpider)

    def test_start_requests_should_return_a_splash_req_to_the_main_page(self):
        s = EmailAddressesSpider('google.com:80')
        start_requests = s.start_requests()
        self.assertEqual(len(start_requests), 1)
        self.assertEqual(type(start_requests[0]), SplashRequest)
        self.assertEqual(start_requests[0].url, 'http://google.com:80')

    def test_sets_allowed_domains_based_on_the_domain_param(self):
        s = EmailAddressesSpider('google.com')
        self.assertEqual(['google.com'], s.allowed_domains)

    def test_removes_port_before_setting_allowed_domains(self):
        s = EmailAddressesSpider('google.com:8000')
        self.assertEqual(['google.com'], s.allowed_domains)

    def test_parse_yields_emails_from_the_response(self):
        values = self.parse_based_on_response_body('a@b.com and c@d.com')
        self.assertEqual(values, [{'email': 'a@b.com'}, {'email': 'c@d.com'}])

    def test_parse_yields_links_from_the_response(self):
        values = self.parse_based_on_response_body(
            '<a href="hello.html">hello</a> and '
            '<a href="http://my.domain/hello">hello</a>')
        self.assertEqual(len(values), 2)
        self.assertEqual(values[0].url, 'http://google.com/hello.html')
        self.assertEqual(values[1].url, 'http://my.domain/hello')

    def test_should_skip_links_to_images_and_videos(self):
        values = self.parse_based_on_response_body(
            '<a href="vid.mp4">vid 1</a>'
            '<a href="vid.mov?a=b&c=d">vid 2</a> and'
            '<a href="hello.html">hello</a> and '
            '<a href="image.jpg">image 1</a> and'
            '<a href="image.png?a=b&c=d">image 2</a>')
        self.assertEqual(len(values), 1)
        self.assertEqual(values[0].url, 'http://google.com/hello.html')

    def parse_based_on_response_body(self, body):
        s = EmailAddressesSpider('google.com')
        resp = TextResponse(body=body, url='http://google.com')
        return list(s.parse(resp))


if __name__ == '__main__':
    unittest.main()
