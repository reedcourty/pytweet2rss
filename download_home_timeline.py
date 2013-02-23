#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import logging
import shelve
import json

import tweepy

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)

logger.info('Start running script')
 
s = shelve.open('homeline-tweets.db')

file = open('API.keys', 'r+')
data = json.load(file)

CONSUMER_KEY = data["CONSUMER_KEY"]
logger.debug('CONSUMER_KEY = {0}'.format(CONSUMER_KEY))

CONSUMER_SECRET = data["CONSUMER_SECRET"]
logger.debug('CONSUMER_SECRET = {0}'.format(CONSUMER_SECRET))                

ACCESS_KEY = data["ACCESS_KEY"]
logger.debug('ACCESS_KEY = {0}'.format(ACCESS_KEY))

ACCESS_SECRET = data["ACCESS_SECRET"]
logger.debug('ACCESS_SECRET = {0}'.format(ACCESS_SECRET))

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)

s['home_timeline'] = api.home_timeline(count=200)
s.close()
