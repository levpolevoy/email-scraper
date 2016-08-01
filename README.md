# Email scraper

A script that prints all of the emails found in a crawl of all of the pages in a specific domain.

## Background

It's an exercise from a job interview.

## Installation

**Clone:**

```
git clone git@github.com:levpolevoy/email-scraper.git
```

**Start a virtualenv (optional):**

```
virtualenv venv
source venv/bin/activate
```

**Install python dependencies:**

```
pip install -r requirements.txt
```

## Running

Quick run:
```
./find_emails.sh DOMAIN
```

More control:
```
rm -f emails.csv
scrapy runspider find_emails.py -L DEBUG -o emails.csv -a domain=doc.scrapy.org
cat emails.csv
```

## Testing

### Live tests

Start a web server with some sample HTML files:
```
cd test-site
python -m SimpleHTTPServer
```

In another shell session, run:

```
./find_emails.sh localhost:8000
```

### Unit testing

```
./test.sh
```

## Design

All of the difficult crawling tasks are deferred to
[scrapy](http://scrapy.org/) - a python web crawling framework.

## File organization

Scrapy crawlers can be organized in one of two ways:

- A project with files with certain naming conventions (similar to Django).
- A single file or any other custom structure.

This is a simple exercise so I thought that it would be easier
to use the single file method (find_emails.py).

## Tasks

- [X] Crawl one page and extract email addresses from it.
- [X] Crawl all of the discoverable pages.
- [X] Limit crawling to one domain.
- [X] Deduplicate the discovered email addresses (see pipelines.py).
- [ ] Print emails as soon as they are found (instead of waiting until processing is over).

## Alternative solutions

### Implement the core crawling manually

The exercise is not complicated, so I could have implemented it
without using a framework like scrapy, but using it made things
easier and in addition I got to learn a little bit about scrapy.

Had I implemented in a more manual manner it would have looked like this:

- Parse CLI params
- Create a queue
- Add the domain index URL to it
- Crawl pages (while the queue is not empty)
    - Download the page using an http library
    - Handle links
        - Extract a list of links from the page
            - Translate them to full URLs (many of them may be relative URLs)
        - Filter URLs that are not in the requested domain
        - Filter URLs that were already processed or are in the queue
        - Add URLs to the queue
    - Handle emails
        - Extract email addresses from the page using a regex over the text content of the page
        - Add the email addresses to a "set()" of email addresses
- Print the set of email addresses

In addition I would have to deal with issues like the following and more:

- Redirects
- Broken links
- Concurrency

### Proprietary solutions

There are online services that can do this task without requiring any coding.

Found via keyword search: *contact scraping*

* https://www.import.io
* https://grabby.io
* http://80legs.com

## Limitations

### No javascript rendering

In the modern web content is often available only after JS was executed.

Such content includes:
- Email addresses
- Links to pages

This script doesn't do any complex pre-processing for a page before
parsing email addresses out of it. It only performs an HTTP GET and
 then parses the body of the response.

Executing javascript is orders of magnitude more complex in terms
of engineering effort, resource requirements and security.

If it's crucial, the [scrapy-splash](https://github.com/scrapy-plugins/scrapy-splash)
project can be helpful.
