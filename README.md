# Email scraper

A script that prints all of the emails found in a crawl of all of the pages in a specific domain.

## Background

This is the solution for an exercise that was given to me as part of a job interview.

## Installation

### Clone

```
git clone git@github.com:levpolevoy/email-scraper.git
```

### Start a virtualenv (optional)

```
virtualenv venv
source venv/bin/activate
```

### Install python dependencies

```
pip install -r requirements.txt
```

### Install and run splash

scrapy-splash in used for executing JavaScript in HTML pages.

Follow the instructions from the
[splash documentation](http://splash.readthedocs.io/en/stable/install.html)

## Running

Make sure that *splash* is running in the background.

Run:
```
./find_emails.sh DOMAIN
```

Examples:

```
./find_emails.sh mit.edu

./find_emails.sh --debug mit.edu
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

### Unit tests

```
./test.sh
```

### Continous integration

See [here](https://circleci.com/gh/levpolevoy/email-scraper).

## Design

All of the difficult crawling tasks are deferred to
[scrapy](http://scrapy.org/) - a python web crawling framework.

## File organization

Scrapy crawlers can be organized in one of two ways:

- A project with files with certain naming conventions (similar to Django).
- A single file or any other custom structure.

This is a simple exercise so I decided to just do it in one file (find_emails.py).

## Tasks

- [X] Crawl one page and extract email addresses from it.
- [X] Crawl all of the discoverable pages.
- [X] Limit crawling to one domain.
- [X] Deduplicate the discovered email addresses.
- [X] Limit the depth of the search to a reasonable number (1-2)
- [X] Skip non-HTML files
- [X] Support JS
- [ ] Print emails as soon as they are found (instead of waiting until processing is over).

## Alternative solutions

### Implement the core crawling manually

The exercise is not complicated, so I could have implemented it
without using a framework like scrapy, but using scrapy made things
easier and in addition I got to learn a bit about scrapy.

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
