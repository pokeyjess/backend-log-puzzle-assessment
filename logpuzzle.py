#!/usr/bin/env python2
"""
python logpuzzle.py animal_code.google.com --todir puzzle

Log Puzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Given an Apache logfile, find the puzzle URLs and download the images.

Here's what a puzzle URL looks like (spread out onto multiple lines):
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US;
rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

__author__ = 'pokeyjess'

import argparse
import os
import re
import sys
from urllib.request import urlretrieve


def read_urls(filename):
    urls = set()
    with open(filename) as f:
        file = f.read()
    photos = re.findall(r'GET \/(.*?\.jpg)', file)
    for photo in photos:
        urls.add("http://" + filename.split("_")[1] + "/" + photo)
    urls_list = set(urls)
    return sorted(urls_list)


def download_images(img_urls, dest_dir):
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    file = '<html>\n\t<body>\n\t\t'
    for i, url in enumerate(img_urls):
        image_name = 'img%d' % i
        print('Retrieving...' + image_name)
        urlretrieve(url, dest_dir + "/" + image_name)
        file += '<img src={}></img>'.format(image_name)
    file += '\n\t</body>\n</html>'
    with open(dest_dir + '/index.html', 'w') as f:
        f.write(file)
    print("Download complete")


def create_parser():
    """Creates an argument parser object."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--todir',
                        help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):
    """Parses args, scans for URLs, gets images from URLs."""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])
