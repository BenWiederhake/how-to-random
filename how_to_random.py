#!/usr/bin/env python3

import argparse
import base64
import bs4
import random
import re
import requests
import sys
import time
from urllib.parse import urlparse


# == Most fragile part: CSS selectors for various interesting tidbits.
# Finding images on a page
WIKIHOW_CANDIDATES = 'li.hasimage>div.largeimage>a[data-href^=\\/Image\\:]'
# Given an image link, how to find the imagedata URL?
WIKIHOW_IMAGE_DATANODE = 'img[src]'
# Given an image link, how to find the uploader?
WIKIHOW_IMAGE_UPLOADER = 'div+p>a'
# Given an image link, how to find the license?
WIKIHOW_IMAGE_LICENSE = 'h3+p>a'

# == Mostly stable
# First contact
WIKIHOW_START = 'https://www.wikihow.com/Special:Randomizer'
# Prefix for absolute path resolution
WIKIHOW_DOMAIN = 'https://www.wikihow.com'

# == Config
# Amount of seconds to wait between each access.
NICE_WAIT_TIME = 3
# Minimal sleep time for grace, in seconds.
NICE_MIN_SLEEP_TIME = 0.1


def nice_get(url, _last_nice_poll=[0]):
    '''
    Access the given URL, and either return the content as a bytestring, or `None`
    if any error occurs.  This function delays invocations in order to guarantee a certain rate limiting.
    '''
    now = time.time()
    until = _last_nice_poll[0] + NICE_WAIT_TIME
    while now < until:
        to_sleep = max(NICE_MIN_SLEEP_TIME, until - now)
        time.sleep(to_sleep)
        now = time.time()
    _last_nice_poll[0] = time.time()
    headers = {'User-Agent': 'HowToRandom/0.1 (https://github.com/BenWiederhake/how-to-random)'}
    r = requests.get(url, headers=headers)
    r.raise_for_status()  # Just crash and abort if anything goes wrong
    return (r.url, r.content)


def make_soup(content):
    return bs4.BeautifulSoup(content, 'lxml')


def determine_candidate(verbose):
    '''
    Let's WikiHow select a random page, fetches it, parses it,
    selects a candidate image, and returns the URL to the "image".
    Note that:
    - If the WikiwHow page contains no images, this process is repeated.
    - By "image URL" I mean something like:
        https://www.wikihow.com/Image:Become-a-Reflexologist-Step-3-Version-2.jpg?ajax=true&aid=1353564
      Note that the imagedata URL, filename, license, and author can be read from this URL.
    '''
    while True:
        if verbose:
            print('Fetching base URL …', file=sys.stderr)
        url, content = nice_get(WIKIHOW_START)
        soup = make_soup(content)
        if verbose:
            print('\tChose {}'.format(url), file=sys.stderr)
        candidates = soup.select(WIKIHOW_CANDIDATES)
        if not candidates:
            if verbose:
                print('\tNo images!', file=sys.stderr)
            continue
        index, chosen = random.choice(list(enumerate(candidates)))
        if verbose:
            print('\tChose #{}: {}'.format(index, chosen['data-href']), file=sys.stderr)
        assert chosen['data-href'].startswith('/')
        return url, index, (WIKIHOW_DOMAIN + chosen['data-href'])


def guess_license(license_url):
    '''
    Attempts to guess a nice name, given a license URL.
    Specifically, we hopefully resolve URLs like
    https://creativecommons.org/licenses/by-nc-sa/3.0/
    to "CC BY-NC-SA 3.0".
    '''

    # Check for CC licenses:
    license_url, success = re.subn('^https://creativecommons\.org/licenses/([a-z-]+)/([0-9.]+)/?$', 'CC \\1 \\2', license_url, 1)
    if success:
        return license_url.upper()

    # # Check for other licenses:
    # license_url, success = re.subn('https://some/thing/', 'foo \\1 bar \\2', license_url, 1)
    # if success:
    #     return license_url

    # TODO: More replacements here?

    # Failed.
    print('WARNING: Could not recognize license URL: {}'.format(license_url),
        file=sys.stderr)
    return None


def scrape_metadata(image_url):
    response = nice_get(image_url)[1]
    if b'All rights reserved.' in response:
        return None

    soup = make_soup(response)

    def select_single(selector):
        selected = soup.select(selector)
        assert len(selected) == 1, \
            'Expected 1 result for selector {}, found {} instead: {}'.format(
                selector, len(selected), selected)
        return selected[0]

    image = select_single(WIKIHOW_IMAGE_DATANODE)
    uploader = select_single(WIKIHOW_IMAGE_UPLOADER)
    license_ = select_single(WIKIHOW_IMAGE_LICENSE)

    metadata = {
        'image': {'url': image['src']},
        'uploader': {'url': WIKIHOW_DOMAIN + uploader['href'], 'name': uploader.text.strip()},
        'license': {'url': license_['href'], 'name': guess_license(license_['href']) or license_.text.strip()},
    }

    return metadata


def fetch_minimum(verbose):
    '''
    Makes as few requests as possible to determine
    the metadata of a random WikiHow image.
    '''
    while True:
        base_url, index, image_url = determine_candidate(verbose)
        if verbose:
            print('\tFetching image metadata …', file=sys.stderr)
        metadata = scrape_metadata(image_url)
        if metadata is None:
            if verbose:
                print('\tNope, no license available.  Restarting …', file=sys.stderr)
            continue
        metadata['choice'] = {'base': base_url, 'base_index': index, 'image_metadata': image_url}
        return metadata


def fill_imagedata(metadata):
    metadata['image']['data'] = nice_get(metadata['image']['url'])[1]


def gather(verbose):
    metadata = fetch_minimum(verbose)
    if verbose:
        print('\tFetching image itself …', file=sys.stderr)
    fill_imagedata(metadata)
    return metadata


def suggest_filename(metadata):
    parsed = urlparse(metadata['image']['url'])
    basename = parsed.path.split('/')[-1]
    parts = basename.split('.')
    # Note that if the filename for some reason does not contain a `.`,
    # this fails gracefully by prepending the license-info.
    extension = parts.pop()
    parts.append(metadata['license']['name'].replace(' ', '-'))
    parts.append(metadata['uploader']['name'].replace(' ', '-'))
    parts.append(extension)
    return '.'.join(parts)


def run_with_options(options):
    if 'file' == options.output:
        metadata = gather(True)
        filename = suggest_filename(metadata)
        with open(filename, 'wb') as fp:
            fp.write(metadata['image']['data'])
        print('Written to {}\nCopyright license seems to be {} with {}:\n\t{}\n\t{}\nHave a great day!'.format(
            filename, metadata['license']['name'], metadata['uploader']['name'],
            metadata['license']['url'], metadata['uploader']['url']))
    elif 'json' == options.output:
        import json
        metadata = gather(False)
        metadata['image']['data_base64'] = base64.encodebytes(metadata['image']['data']).decode('ascii')
        del metadata['image']['data']
        print(json.dumps(metadata, separators=(',', ':'), sort_keys=True))


def make_parser(progname):
    parser = argparse.ArgumentParser(
        prog=progname, description='Shows you a "random" image from wikiHow.')
    parser.add_argument(
        '--output', choices=['json', 'file'], default='file', help='''
            Select thy type of output.

            "file" means that the image file will be written to disk,
            and metadata is written to stdout. This is easily usable for humans.

            "json" means that both image data and metadata are written
            as JSON to stdout. This is easier for scripting.''')
    return parser


def run():
    options = make_parser(sys.argv[0]).parse_args(sys.argv[1:])
    run_with_options(options)


if __name__ == '__main__':
    run()
