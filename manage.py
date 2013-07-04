#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
import logging
import shelve
import json

import tweepy

from flask import Flask
from flask.ext.script import Manager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)
logger.info('Starting...')

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))
    
activate_this = PROJECT_PATH + '/venv/Scripts/activate_this.py'
logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))
    
execfile(activate_this, dict(__file__=activate_this))

app = Flask(__name__)

manager = Manager(app)

@manager.command
def download_home_timeline():    
    os.system(PROJECT_PATH + '/venv/Scripts/python.exe ' + PROJECT_PATH + '/download_home_timeline.py')
    
@manager.command
def get_status(status):
    logger.debug('Status ID = {}'.format(status))

    s = shelve.open(PROJECT_PATH + '/tweet-{}.db'.format(status))

    file = open(PROJECT_PATH + '/API.keys', 'r+')
    data = json.load(file)
    
    CONSUMER_KEY = data["CONSUMER_KEY"]
    CONSUMER_SECRET = data["CONSUMER_SECRET"]              
    ACCESS_KEY = data["ACCESS_KEY"]
    ACCESS_SECRET = data["ACCESS_SECRET"]
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    
    try:
        tweet = None
        api = tweepy.API(auth)
        tweet = api.get_status(status)
        
        logger.debug('tweet.text = {}'.format(tweet.text.encode('UTF-8')))
        
    except tweepy.error.TweepError as e:
        logger.debug('Bajok vannak: {0}'.format(e))
        pass
    if tweet != None:
        s['tweet'] = tweet
    s.close()

if __name__ == "__main__":
    manager.run()