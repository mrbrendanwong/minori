#!/usr/bin/env python3

import argparse
import sqlite3
import datetime
from pprint import pprint


class Minori:
    def __init__(self, db='database.db'):
        self.db = db
        self.connection = sqlite3.connect(self.db)

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def initialize(self):
        self.connection.execute('''CREATE TABLE IF NOT EXISTS shows
             (name text primary key, max_episodes integer, most_recent_episode integer,\
                     keywords text, date_added timestamp)''')
        self.connection.execute('''CREATE TABLE IF NOT EXISTS rss
             (name text primary key, url text, date_added timestamp)''')
        print("initialize::Created database")

    def add_rss(self, name, url):
        date = datetime.datetime.now()
        sql_statement = 'INSERT INTO rss VALUES (?, ?, ?)'
        try:
            self.connection.execute(sql_statement, (name, url, date))
        except sqlite3.IntegrityError:
            print("add_show::RSS already exists in database")
            return

    def add_show(self, name, max_ep, keywords, current=0):
        date = datetime.datetime.now()
        sql_statement = 'INSERT INTO shows VALUES (?, ?, ?, ?, ?)'
        try:
            self.connection.execute(sql_statement, (name, int(max_ep), int(current), keywords, date))
        except sqlite3.IntegrityError:
            print("add_show::Show already exists in database")
            return

        print("add_show::Added show!")

    def get_all_shows(self):
        try:
            sql_statement = 'SELECT * FROM shows'
            shows = [r for r in self.connection.execute(sql_statement)]
            print("SHOWNAME | MAX_EPS | CURRENT_EP | DATE_ADDED")
            pprint(shows)
        except sqlite3.OperationalError:
            print("Database not initialized")

    def get_all_rss(self):
        try:
            sql_statement = 'SELECT * FROM rss'
            rss = [r for r in self.connection.execute(sql_statement)]
            print("RSS Name | RSS URL")
            pprint(rss)
        except sqlite3.OperationalError:
            print("Database not initialized")



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

    rss_subparser = subparser.add_parser('addrss', help='Add RSS subs')
    rss_subparser.add_argument('name', help='Name of the RSS feed')
    rss_subparser.add_argument('url', help='Direct to RSS feed')
    rss_subparser.set_defaults(which='addrss')

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

    if args.which == 'addrss':
        name = args.name
        url = args.url
        minori.add_rss(name, url)


if __name__ == '__main__':
    main()
