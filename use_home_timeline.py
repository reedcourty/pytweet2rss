#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import logging
import shelve

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)

logger.info('Start running script')
 
s = shelve.open('homeline-tweets.db')

home_timeline_array = s['home_timeline']

for tweet in home_timeline_array:
    logger.debug('tweet.author.screen_name = {0}'.format(tweet.author.screen_name))
    logger.debug('tweet.created_at = {0}'.format(tweet.created_at))
    logger.debug('tweet.text = {0}'.format(tweet.text.encode('UTF-8')))

s.close()
