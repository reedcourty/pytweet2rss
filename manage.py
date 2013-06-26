#!/usr/bin/env python
# -*- coding: utf-8 -*- #

import os
import logging

from flask import Flask
from flask.ext.script import Manager

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s -- %(levelname)s : %(name)s -- %(message)s')
logger = logging.getLogger(__name__)
logger.info('Starting...')

app = Flask(__name__)

manager = Manager(app)

@manager.command
def download_home_timeline():    
    
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))
    
    activate_this = PROJECT_PATH + '/venv/Scripts/activate_this.py'
    logger.debug('PROJECT_PATH = {0}'.format(PROJECT_PATH))
    
    execfile(activate_this, dict(__file__=activate_this))
    
    os.system(PROJECT_PATH + '/venv/Scripts/python.exe ' + PROJECT_PATH + '/download_home_timeline.py')

if __name__ == "__main__":
    manager.run()