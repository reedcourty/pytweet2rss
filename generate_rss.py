#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import logging
import time
import shelve
import datetime
import os
import re

import PyRSS2Gen
import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)

IMAGE_HEIGHT = '256px'

logger.info('Start running script')

def get_local_time_offset():
    t = time.time()
        
    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone
    
def url_contents_tumblr_media(tweet):
    url = tweet.entities['urls'][0]['expanded_url']
    regexp = r'http[s]{0,1}:\/\/(\d)+\.media\.tumblr\.com'
    return (len(re.findall(regexp, url))!=0)

def is_instagram_link(tweet):
    url = tweet.entities['urls'][0]['expanded_url']
    regexp = r'http[s]{0,1}:\/\/instagram.com\/'
    return (len(re.findall(regexp, url))!=0)

def url_contents_some_media(tweet):
    url = tweet.entities['urls'][0]['expanded_url']
    regexp = r'^http[s]{0,1}:\/\/.+\.(jpg|png)$'
    return (len(re.findall(regexp, url))!=0)

def get_instagram_media(url):
    logger.debug('get_instagram_media -> url = {0}'.format(url))
    r = requests.get(url)
    
    soup = BeautifulSoup(r.content)

    l = []
    script_list = soup.find_all('script')
    for script in script_list:
        try:
            src = script['src']        
        except KeyError as e:
            l.append(script)
    
    for script in l:
        if (str(script).find("window._jscalls")!=-1):
            workitem = str(script)
    
    workitem = workitem[workitem.find("display_src")+len("display_src")+3:len(workitem)]
    img_src = workitem[0:workitem.find('"')].replace("\\", "")

    logger.debug('get_instagram_media -> img_src = {0}'.format(img_src))
        
    new_img = '<img src="{}" height="{}"/>'.format(img_src, IMAGE_HEIGHT)
    
    return new_img
    
    
def create_rss_item(tweet):    
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
    
    user_mentions_size = len(tweet.entities['user_mentions'])
    logger.debug('user_mentions_size = {0}'.format(user_mentions_size))
        
    if (user_mentions_size > 0):
        for user_mention in tweet.entities['user_mentions']:
            logger.debug('user_mention = {0}'.format(user_mention))
            
            screen_name_url = '<a href="https://twitter.com/{0}">{0}</a>'.format(user_mention['screen_name'])
            logger.debug('screen_name_url = {0}'.format(screen_name_url))
            
            resc = re.compile(re.escape(user_mention['screen_name'].encode('UTF-8')), re.IGNORECASE)
            content = resc.sub(screen_name_url.encode('UTF-8'), content)          
            
            logger.debug('content = {0}'.format(content))
            
    urls_size = len(tweet.entities['urls'])
    logger.debug('urls_size = {0}'.format(urls_size))
    
    if (urls_size > 0):
        for url in tweet.entities['urls']:
            logger.debug('url = {0}'.format(url))
            
            logger.debug('url = {0}'.format(url['url'].encode('UTF-8')))
            logger.debug('display_url = {0}'.format(url['display_url'].encode('UTF-8')))
            logger.debug('expanded_url = {0}'.format(url['expanded_url'].encode('UTF-8')))
            
            if (url_contents_tumblr_media(tweet)):
                r_url = u'<img src="{0}" height="{1}"/>'.format(url['expanded_url'].encode('UTF-8'), IMAGE_HEIGHT)
                logger.debug('r_url = {0}'.format(r_url)) 
            elif (url_contents_some_media(tweet)):
                r_url = u'<img src="{0}" height="{1}"/>'.format(url['expanded_url'].encode('UTF-8'), IMAGE_HEIGHT)
                logger.debug('r_url = {0}'.format(r_url))
            else:
                r_url = u'<a href="{0}">{0}</a>'.format(url['expanded_url'].encode('UTF-8'))
                logger.debug('r_url = {0}'.format(r_url))
                
            if is_instagram_link(tweet):
                r_url = u'<a href="{0}">{1}</a>'.format(url['expanded_url'].encode('UTF-8'), get_instagram_media(url['expanded_url'].encode('UTF-8')))
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
            
            #img_width = media['sizes']['small']['w']
            #logger.debug("img_width = {0}".format(img_width))
            
            u = media['url']
            logger.debug('u = {0}'.format(u))
            
            media_url = media['media_url_https']
            logger.debug('media_url = {0}'.format(media_url))
            
            r_u = u'<a href={0}><img src={1} height="{2}"/><a/>'.format(u, media_url, IMAGE_HEIGHT)
            
            content = content.replace(u.encode('UTF-8'), r_u.encode('UTF-8'))
            logger.debug('content = {0}'.format(content))
    
    hashtags_len = len(tweet.entities['hashtags'])
    logger.debug('hashtags_len = {0}'.format(hashtags_len))
    
    if (hashtags_len>0):
        for hashtag in tweet.entities['hashtags']:
            logger.debug('hashtag = {0}'.format(hashtag))
            
            hashtag_text = hashtag['text'].encode('UTF-8')
            logger.debug('hashtag_text = {0}'.format(hashtag_text))
            
            hashtag_url = 'https://twitter.com/search?q=%23{0}&src=hash'.format(hashtag_text)
            logger.debug('hashtag_url = {0}'.format(hashtag_url))
            
            hashtag_text = '#' + hashtag_text
            r = '<a href="{0}">{1}</a>'.format(hashtag_url, hashtag_text.replace('#', '<font style="color: rgb(122, 109, 241);">#</font>'))
            logger.debug('r = {0}'.format(r))
            
            content = content.replace(hashtag_text, r)
            logger.debug('content = {0}'.format(content))
            
    content = content.replace('@', '<font style="color: rgb(122, 109, 241);">@</font>')
    
    description = '<img src="{0}" width="48px"/>'.format(tweet.user.profile_image_url_https)
    
    description = description + '<a href="https://twitter.com/{0}">{0}</a>: '.format(tweet.author.screen_name)
    logger.debug('description = {0}'.format(description))
    
    description = description + content + "<br /><br />"
    logger.debug('description = {0}'.format(description))
    
    
    
    local_time_offset = get_local_time_offset()
    logger.debug('local_time_offset = {0}'.format(local_time_offset))
    logger.debug('tweet.created_at = {0}'.format(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")))
    
    created_at = tweet.created_at + datetime.timedelta(seconds=local_time_offset)
    logger.debug('created_at = {0}'.format(created_at.strftime("%Y-%m-%d %H:%M:%S")))
    
    description = description + u"Világgá kürtölve: {0}".format(created_at.strftime("%Y-%m-%d %H:%M:%S")).encode("UTF-8")    
    
    logger.debug('description = {0}'.format(description))
    
    link = "https://twitter.com/" + tweet.author.screen_name + "/status/" + tweet.id_str
    
    rss_item = PyRSS2Gen.RSSItem(
        title = '{0}: {1}'.format(tweet.author.screen_name, tweet.text.encode('UTF-8')),
        author = tweet.author.screen_name,
        link = link,
        description = description,
        guid = PyRSS2Gen.Guid(link),
        pubDate = tweet.created_at) # Úgy néz ki, hogy az UTC-t kell megadni
    
    rss.items.append(rss_item)

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))

XML_PATH = PROJECT_PATH + "/timeline.xml"
logger.debug('XML_PATH = {0}'.format(XML_PATH))

DB_PATH = PROJECT_PATH + "/homeline-tweets.db"
logger.debug('DB_PATH = {0}'.format(DB_PATH))

s = shelve.open(DB_PATH)

rss = PyRSS2Gen.RSS2(
    title = "reedcourty's Twitter homeline",
    link = "http://ratucen.sch.bme.hu/mrkdev/static/timeline.xml",
    description = "Twitter homeline",
    items = [])

try:
    home_timeline = s['home_timeline']

    for tweet in home_timeline:
        create_rss_item(tweet)
except KeyError as e:
    tweet = s['tweet']
    create_rss_item(tweet)

rss.lastBuildDate = datetime.datetime.now()

rss.write_xml(open(XML_PATH, "w"), encoding="UTF-8")    
   
s.close()
