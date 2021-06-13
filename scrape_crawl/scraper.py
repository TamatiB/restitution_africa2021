#!/usr/bin/python3.8
'''
Created on 27 May 2021AD
@author: Pelonomi Moiloa

Scraper to scrape media houses for discussion on African
Artifact restitution.

Paused this because I dont know the media houses and what that
will look like, need more info
'''

import scrapy
from config import SET_SELECTOR

class MediaSpider(scrapy.Spider): #child class
    name = "media_spider" #spider name
    start_urls = ['http://brickset.com/sets/year-2016']

    def parse(self, response):
        SET_SELECTOR = '.set'
        for brickset in response.css(SET_SELECTOR):
            pass
