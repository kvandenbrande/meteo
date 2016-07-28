#!/bin/python
# -*- coding: utf-8 -*-
#__author__ = "Kevin Van den Brande"


import urllib.request
from urllib.request import urlopen
import json
import shutil
import os
import time
from tweet import tweet_message


#Weerbericht van aan zee op twitter


def meteo():
    get_picture()
    time.sleep(15)
    send_tweet()
    time.sleep(30)
    delete_picture()
    
    

def get_weather():
    f = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/conditions/lang:NL/q/pws:IVLAAMSG89.json')
    json_string = f.read().decode('utf-8')
    parsed_json = json.loads(json_string)
    #temperatuur
    temp_c = parsed_json['current_observation']['temp_c']
    #status
    weather = parsed_json['current_observation']['weather']
    #kans op neerslag
    rain = get_POP()
    t_rain = "% kans op neerslag"
    #windrichting
    wind_dir = parsed_json['current_observation']['wind_dir']
    #windsnelheid
    wind_gust_kph = parsed_json['current_observation']['wind_gust_kph']
    f.close()
    return ("%s; %s°C; %s%s; wind: %skm/h %s" % (weather, temp_c, rain, t_rain, wind_gust_kph, wind_dir))
    

def get_POP():
    h = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/hourly/lang:NL/q/pws:IVLAAMSG89.json')
    json_string = h.read().decode('utf-8')
    parsed_json = json.loads(json_string)
    #POP
    hourly = parsed_json['hourly_forecast']
    rain = hourly[0]['pop']
    h.close()
    return (rain)
    

def get_UV():
    g = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/conditions/lang:NL/q/pws:IDEHAAN12.json')
    json_string = g.read().decode('utf-8')
    parsed_json = json.loads(json_string)
    #UV
    UV = parsed_json['current_observation']['UV']
    g.close()
    if int(UV) < 4:
        return (" ")
    else:
        return ("; UV-index:%s " % (UV))
    

def get_message():
    hashtag = "#weer #dekust"
    message = get_weather() + get_UV() + hashtag
    return(message)

	
def get_picture():
    try:
        urllib.request.urlretrieve("http://www.kustweerbericht.be/inter/webcam/webcam/npt.jpg", "wb.jpg")
    except URLError:
        get_backup_picture()


def get_backup_picture():
    srcfile ='/home/pi/Desktop/meteo/backup/wb.jpg'
    destination ='/home/pi/Desktop/meteo/'
    shutil.copy(srcfile, dstdir)


def send_tweet():
    picture = '/home/pi/Desktop/meteo/wb.jpg'  
    message = get_message()
    tweet_message(picture,message) 


def delete_picture():
    os.remove("wb.jpg")
    

meteo()

