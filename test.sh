#!/usr/bin/env bash

set -x
set -e

pep8 *.py -v
python test_find_emails.py
