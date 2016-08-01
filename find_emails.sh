#!/usr/bin/env bash

set -e

DOMAIN="$1"
if [[ -z "$DOMAIN" ]] ; then
    echo -e "ERROR: Must specify a domain.\n"
    echo "Usage: $0 DOMAIN"
    exit 1
fi

OUTPUT="emails_${DOMAIN}.csv"
rm -f ${OUTPUT}
scrapy runspider find_emails.py -L ERROR -o ${OUTPUT} -a domain=${DOMAIN}
cat ${OUTPUT}
rm -f ${OUTPUT}
