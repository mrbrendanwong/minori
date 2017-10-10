#!/usr/bin/env python3

import argparse
from minori.minori import Minori


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--initdb', help='Initialize database <name>')
    parser.add_argument('--shows', help='Get all shows in the database', action='store_true')
    parser.add_argument('--rss', help='Get all rss feed in the database', action='store_true')

    subparser = parser.add_subparsers(dest='which')
    add_subparser = subparser.add_parser('addshow', help='Add a show')
    add_subparser.add_argument('name', help='Show name')
    add_subparser.add_argument('max', help='Max total episodes for the show')
    add_subparser.add_argument('keyword', help='Keywords to search for, csv (eg "Commie,720p).\
                                                No need to provide show name')
    add_subparser.add_argument('--current', help='Current episode (defaults to 0, no ep\'\
                                                  watched)', action='store_true')
    add_subparser.set_defaults(which='addshow')

    rmshow_subparser = subparser.add_parser('rmshow', help='Remove a show')
    rmshow_subparser.add_argument('name', help='Comma-separated list of shows to remove')
    rmshow_subparser.set_defaults(which='rmshow')

    rss_subparser = subparser.add_parser('addrss', help='Add RSS subs')
    rss_subparser.add_argument('name', help='Name of the RSS feed')
    rss_subparser.add_argument('url', help='Direct to RSS feed')
    rss_subparser.set_defaults(which='addrss')

    rmrss_subparser = subparser.add_parser('rmrss', help='Remove a RSS feed')
    rmrss_subparser.add_argument('name', help='Comma-separated list of RSS feeds to remove')
    rmrss_subparser.set_defaults(which='rmrss')

    args = parser.parse_args()

    minori = Minori()
    if args.initdb:
        minori.initialize()

    if args.shows:
        minori.get_all_shows()

    if args.rss:
        minori.get_all_rss()

    if args.which == 'addshow':
        name = args.name
        max_ep = args.max
        current = args.current
        keyword = args.keyword
        minori.add_show(name, max_ep, keyword, current)
    elif args.which == 'rmshow':
        name = args.name.split(',')
        minori.rm_show(name)

    if args.which == 'addrss':
        name = args.name
        url = args.url
        minori.add_rss(name, url)
    elif args.which == 'rmrss':
        name = args.name.split(',')
        minori.rm_rss(name)


if __name__ == '__main__':
    main()
