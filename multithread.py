#!/usr/bin/python

from multiprocessing.dummy import Pool as ThreadPool 
import subprocess
import logging
import os
import sys

FILE_URLS = 'urls.txt';
SAVE_DIRECTORY = '/var/tmp/downloaded/'
MAX_DEPTH = 0

MAX_THREAD = 4
LOG_DIRECTORY = "log"
LAST_URL_FILE = "%s/last_url.log" % LOG_DIRECTORY

def get_last_url():
	if os.path.exists(LAST_URL_FILE):
		return open(LAST_URL_FILE).readlines()[0]
	else:
		return False

def log_last_url(url):
	with open(LAST_URL_FILE, "w") as last_url_file:
		last_url_file.write(url)

def worker(url):
	command = "python crawler.py -d {0} -u -p \"{1}\" \"{2}\"".format(MAX_DEPTH, SAVE_DIRECTORY, url) 
	log_last_url(url)
	subprocess.Popen(command, shell=True)

def main():

	# todo: relocate!
	logging.basicConfig(level=logging.DEBUG,
	                    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
	                    )

	if not os.path.exists(FILE_URLS):
		print >> sys.stderr, "File \"%s\" with URLs not exists!" % FILE_URLS
		raise SystemExit, 0

	# split urls from file
	URLS = open(FILE_URLS).read().split('\n')

	# create log directory
	if not os.path.exists(LOG_DIRECTORY):
		os.makedirs(LOG_DIRECTORY)
	
	# last processed urls
	tmp_urls = []
	last_url = get_last_url()
	if last_url is not False:		
		append = False
		for url in URLS:
			if url == last_url:
				append = True
				
			if append is True:
				tmp_urls.append(url)
	else:
		tmp_urls = URLS

	# filter empty value
	urls = filter(lambda x: len(x) > 0, tmp_urls) 

	# pool threads
	pool = ThreadPool(MAX_THREAD) 
	results = pool.map(worker, urls)

	pool.close() 
	pool.join() 

if __name__ == "__main__":
    main()