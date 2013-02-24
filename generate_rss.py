#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import logging
import shelve
import datetime
import os
import re

import PyRSS2Gen

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)

logger.info('Start running script')

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))

XML_PATH = PROJECT_PATH + "timeline.xml"
logger.debug('XML_PATH = {0}'.format(XML_PATH))

s = shelve.open('homeline-tweets.db')

rss = PyRSS2Gen.RSS2(
    title = "reedcourty's Twitter homeline",
    link = "http://ratucen.sch.bme.hu/mrkdev/static/timeline.xml",
    description = "Twitter homeline",
    items = [])

home_timeline = s['home_timeline']

for tweet in home_timeline:
    logger.debug('######################################################################################################')
    logger.debug('tweet.author.screen_name = {0}'.format(tweet.author.screen_name))
    logger.debug('tweet.contributors = {0}'.format(tweet.contributors))
    logger.debug('tweet.tweet.coordinates = {0}'.format(tweet.coordinates))
    logger.debug('tweet.created_at = {0}'.format(tweet.created_at))
    logger.debug('tweet.destroy = {0}'.format(tweet.destroy))
    logger.debug('tweet.entities = {0}'.format(tweet.entities))
    logger.debug('tweet.favorite = {0}'.format(tweet.favorite))
    logger.debug('tweet.favorited = {0}'.format(tweet.favorited))
    logger.debug('tweet.geo = {0}'.format(tweet.geo))
    logger.debug('tweet.id = {0}'.format(tweet.id))
    logger.debug('tweet.id_str = {0}'.format(tweet.id_str))
    logger.debug('tweet.in_reply_to_screen_name = {0}'.format(tweet.in_reply_to_screen_name))
    logger.debug('tweet.in_reply_to_status_id = {0}'.format(tweet.in_reply_to_status_id))
    logger.debug('tweet.in_reply_to_status_id_str = {0}'.format(tweet.in_reply_to_status_id_str))
    logger.debug('tweet.in_reply_to_user_id = {0}'.format(tweet.in_reply_to_user_id))
    logger.debug('tweet.in_reply_to_user_id_str = {0}'.format(tweet.in_reply_to_user_id_str))
    logger.debug('tweet.parse = {0}'.format(tweet.parse))
    logger.debug('tweet.parse_list = {0}'.format(tweet.parse_list))
    logger.debug('tweet.place = {0}'.format(tweet.place))
    try:
        logger.debug('tweet.possibly_sensitive = {0}'.format(tweet.possibly_sensitive))
    except AttributeError:
        pass
    logger.debug('tweet.retweet = {0}'.format(tweet.retweet))
    logger.debug('tweet.retweet_count = {0}'.format(tweet.retweet_count))
    logger.debug('tweet.retweeted = {0}'.format(tweet.retweeted))
    logger.debug('tweet.retweets = {0}'.format(tweet.retweets))
    logger.debug('tweet.source = {0}'.format(tweet.source.encode('UTF-8')))
    logger.debug('tweet.source_url = {0}'.format(tweet.source_url))
    logger.debug('tweet.text = {0}'.format(tweet.text.encode('UTF-8')))
    logger.debug('tweet.truncated = {0}'.format(tweet.truncated))
    logger.debug('tweet.user = {0}'.format(tweet.user))
    
    logger.debug('tweet.user.profile_image_url_https = {0}'.format(tweet.user.profile_image_url_https))  
            
    content = tweet.text.encode('UTF-8')
    logger.debug('content = {0}'.format(content))
    
    um_len = len(tweet.entities['user_mentions'])
    
    logger.debug('um_len = {0}'.format(um_len))
        
    if (um_len > 0):
        for user_mention in tweet.entities['user_mentions']:
            logger.debug('user_mention = {0}'.format(user_mention))
            
            sn_url = '<a href="https://twitter.com/{0}">{0}</a>'.format(user_mention['screen_name'])
            logger.debug('sn_url = {0}'.format(sn_url))
            
            resc = re.compile(re.escape(user_mention['screen_name'].encode('UTF-8')), re.IGNORECASE)
            content = resc.sub(sn_url.encode('UTF-8'), content)          
            
            logger.debug('content = {0}'.format(content))
            
    u_len = len(tweet.entities['urls'])
    logger.debug('u_len = {0}'.format(u_len))
    
    if (u_len > 0):
        for url in tweet.entities['urls']:
            logger.debug('url = {0}'.format(url))
            
            logger.debug('display_url = {0}'.format(url['display_url'].encode('UTF-8')))
            logger.debug('expanded_url = {0}'.format(url['expanded_url'].encode('UTF-8')))
            
            r_url = u'<a href="{0}">{0}</a>'.format(url['url'].encode('UTF-8'))
            logger.debug('r_url = {0}'.format(r_url))          
            
            content = content.replace(url['url'].encode('UTF-8'), r_url.encode('UTF-8'))
            logger.debug('content = {0}'.format(content))
            
    try:
        media_len = len(tweet.entities['media'])
    except KeyError:
        media_len = 0
    logger.debug('media_len = {0}'.format(media_len))
    
    if (media_len > 0):
        for media in tweet.entities['media']:
            u = media['url']
            logger.debug('u = {0}'.format(u))
            
            media_url = media['media_url_https']
            logger.debug('media_url = {0}'.format(media_url))
            
            r_u = u'<a href={0}><img src={1} /><a/>'.format(u, media_url)
            
            content = content.replace(u.encode('UTF-8'), r_u.encode('UTF-8'))
            logger.debug('content = {0}'.format(content))
    
    description = '<img src="{0}" />'.format(tweet.user.profile_image_url_https)
    
    description = description + '<a href="https://twitter.com/{0}">{0}</a>: '.format(tweet.author.screen_name)
    logger.debug('description = {0}'.format(description))
    
    description = description + content + "<br /><br />"
    logger.debug('description = {0}'.format(description))
    
    description = description + u"Világgá kürtölve: {0}".format(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")).encode("UTF-8")    
    
    logger.debug('description = {0}'.format(description))
    
    link = "https://twitter.com/" + tweet.author.screen_name + "/status/" + tweet.id_str
    
    rss_item = PyRSS2Gen.RSSItem(
        title = '{0}: {1}'.format(tweet.author.screen_name, tweet.text.encode('UTF-8')),
        author = tweet.author.screen_name,
        link = link,
        description = description,
        guid = PyRSS2Gen.Guid(link),
        pubDate = tweet.created_at)
    
    rss.items.append(rss_item)

rss.lastBuildDate = datetime.datetime.now()

rss.write_xml(open("timeline.xml", "w"), encoding="UTF-8")    
   
s.close()
