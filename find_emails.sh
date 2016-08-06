#!/usr/bin/env bash

set -e

usage() {
    cat<<EOF
Usage: $0 [OPTIONS] DOMAIN

Optional params:
    --debug     print debug information
    --help      print this help section
EOF
    exit 1
}

parse_args() {
    while [[ ! -z "$1" ]] ; do
        case "$1" in
            --debug) LOG_LEVEL="DEBUG";;
            --help) usage;;
            *) DOMAIN="$1";;
        esac
        shift
    done

    if [[ -z "$DOMAIN" ]] ; then
        echo -e "ERROR: Must specify a domain.\n"
        usage
    fi
}

crawl_and_print_emails() {
    OUTPUT="emails_${DOMAIN}.csv"
    rm -f ${OUTPUT}
    scrapy runspider find_emails.py -L ${LOG_LEVEL} -o ${OUTPUT} -a domain=${DOMAIN}
    cat ${OUTPUT}
    rm -f ${OUTPUT}
}

DOMAIN=""
LOG_LEVEL="ERROR"

parse_args $@
crawl_and_print_emails
