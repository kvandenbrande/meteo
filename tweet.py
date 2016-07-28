#!/bin/python
# -*- coding: utf-8 -*-
#__author__ = "Kevin Van den Brande"

import tweepy
import os
import configparser
import inspect

path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# read config
config = configparser.SafeConfigParser()
config.read(os.path.join(path, "config"))

# create bot
auth = tweepy.OAuthHandler(config.get("twitter","consumer_key"), config.get("twitter","consumer_secret"))
auth.set_access_token(config.get("twitter","access_token"), config.get("twitter","access_token_secret"))
api = tweepy.API(auth)


def tweet_message(picture,message):
    api.update_with_media(picture, status=message)
    return
