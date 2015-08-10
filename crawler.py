#!/usr/bin/env python
#-*- coding:utf-8 -*-

""" Web Crawler/Spider

This module implements a web crawler. This is very _basic_ only
and needs to be extended to do anything usefull with the
traversed pages.

Base on https://github.com/ewa/python-webcrawler.
"""

import re
import os
import sys
import time
import math
import urllib2
import urlparse
import optparse
import logging
import requests

from lib.link import Link
from lib.crawler import Crawler
from lib.fetcher import Fetcher
from lib.dotwriter import DotWriter
from lib.fetcher import AGENT as USER_AGENT

__version__ = "1.3.1"
__copyright__ = "2015 Lukas Mestan"
__license__ = "MIT"
__author__ = "Lukas Mestan"
__author_email__ = "lukas.mestan@gmail.com"

USAGE = "%prog [options] <url>"
VERSION = "%prog v" + __version__

LOG_DIRECTORY = "log"

def getLinks(url):
    page = Fetcher(url)
    page.fetch()
    for i, url in enumerate(page):
        print "%d. %s" % (i, url)

def parse_options():
    """ parse_options() -> opts, args
    Parse any command-line options given returning both
    the parsed options and arguments.
    """

    parser = optparse.OptionParser(usage=USAGE, version=VERSION)

    parser.add_option("-q", "--quiet",
            action="store_true", default=False, dest="quiet",
            help="Enable quiet mode")

    parser.add_option("-l", "--links",
            action="store_true", default=False, dest="links",
            help="Get links for specified url only")    

    parser.add_option("-d", "--depth",
            action="store", type="int", default=0, dest="depth_limit",
            help="Maximum depth to traverse")

    parser.add_option("-c", "--confine",
            action="store", type="string", dest="confine",
            help="Confine crawl to specified prefix")

    parser.add_option("-x", "--exclude", action="append", type="string",
                      dest="exclude", default=[], help="Exclude URLs by prefix")
    
    parser.add_option("-L", "--show-links", action="store_true", default=False,
                      dest="out_links", help="Output links found")

    parser.add_option("-u", "--show-urls", action="store_true", default=False,
                      dest="out_urls", help="Output URLs found")

    parser.add_option("-D", "--dot", action="store_true", default=False,
                      dest="out_dot", help="Output Graphviz dot file")
    
    parser.add_option("-p", "--path", action="store", type="string", 
                      dest="out_path", default=False, help="Output path directory")

    opts, args = parser.parse_args()

    #if not opts.out_path: 
    #    parser.print_help(sys.stderr)
    #    parser.error('output path not given (options -p)')

    if len(args) < 1:
        parser.print_help(sys.stderr)
        raise SystemExit, 1

    if opts.out_links and opts.out_urls:
        parser.print_help(sys.stderr)
        parser.error("options -L and -u are mutually exclusive")

    return opts, args

def toSeoFriendly(s, maxlen):
    """ Join with dashes, eliminate punction, clip to maxlen, lowercase.
        >>> ToSeoFriendly("The quick. brown4 fox jumped", 14)
        'the-quick-brow'
    """

    t = '-'.join(s.split())                                # join words with dashes
    u = ''.join([c for c in t if c.isalnum() or c=='-'])   # remove punctation   
    return u[:maxlen].rstrip('-').lower()                  # clip to maxlen

def main():   

    opts, args = parse_options()

    url = args[0]

    if opts.links:
        getLinks(url)
        raise SystemExit, 0

    depth_limit = opts.depth_limit
    confine_prefix = opts.confine
    exclude = opts.exclude

    sTime = time.time()

    print >> sys.stderr, "Crawling %s (Max Depth: %d)" % (url, depth_limit)
    crawler = Crawler(url, depth_limit, confine_prefix, exclude)
    crawler.crawl()

    # create log directory
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)

    num_links = 0
    if opts.out_urls:
        for url_crawl in crawler.urls_seen:

            parsed_uri = urlparse.urlparse(url_crawl)
            
            # only base url
            if not re.match(".*%s" % parsed_uri.netloc.replace('www.', ''), url): # and not opts.skip_host:
                continue

            if not opts.out_path:
                print url_crawl
            else:
                domain = '{uri.netloc}'.format(uri=parsed_uri)
                log_file = "%s/%s.log" % (LOG_DIRECTORY, domain)

                logging.basicConfig(
                    filename=log_file,
                    filemode='w+',
                    level=logging.DEBUG,
                    format='%(asctime)-15s [%(levelname)s] (%(threadName)-10s) %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                )
                
                try:
                    directory = opts.out_path + domain + '/'
                    path = directory + toSeoFriendly(url_crawl, 50) + '.html'
                    
                    if not os.path.exists(directory):
                        os.makedirs(directory)

                    r = requests.get(url_crawl, allow_redirects=True, timeout=30)
                    if not os.path.exists(path):
                        target = open(path, 'w')
                        target.write(r.text.encode('utf-8'))
                        target.close()

                        num_links = num_links + 1
                        logging.debug("Saving: {0}".format(url_crawl))

                except IOError as e:
                    logging.error("IOError: {0} {1}".format(url, e.message))
                    pass

                except Exception as e:
                    logging.error("Error({0}): {1}".format(url, e.__doc__, e.message), exc_info=True)
                    pass

    if opts.out_links:
        print "\n".join([str(l) for l in crawler.links_remembered])
        
    if opts.out_dot:
        d = DotWriter()
        d.asDot(crawler.links_remembered)

    eTime = time.time()
    tTime = eTime - sTime

    print >> sys.stderr, "Found:    %d" % num_links
    print >> sys.stderr, "Stats:    (%d/s after %0.2fs)" % (
            int(math.ceil(float(num_links) / tTime)), tTime)

if __name__ == "__main__":
    main()
