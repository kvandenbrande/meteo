#!/bin/python
# -*- coding: utf-8 -*-
#__author__ = "Kevin Van den Brande"


import urllib.request
from urllib.request import urlopen
import json
import shutil
import os, sys
import time
from tweet import tweet_message
from internet import is_connected


#Weerbericht van aan zee op twitter


def meteo():
    if is_connected()==True:
        get_picture()
        time.sleep(15)
        get_weather()
        send_tweet()
        time.sleep(30)
        delete_picture()
        sys.exit()
    else:
        sys.exit()    



def get_weather():
    x = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/hourly/lang:NL/q/pws:IVLAAMSG89.json')
    x_json_string = x.read().decode('utf-8')
    global pop_parsed
    pop_parsed = json.loads(x_json_string)
    x.close()
    time.sleep(1)
    y = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/conditions/lang:NL/q/pws:IDEHAAN12.json')
    y_json_string = y.read().decode('utf-8')
    global uv_parsed
    uv_parsed = json.loads(y_json_string)
    y.close()
    time.sleep(1)
    z = urlopen('http://api.wunderground.com/api/e3afd129ef7787a4/conditions/lang:NL/q/pws:IVLAAMSG89.json')
    z_json_string = z.read().decode('utf-8')
    global weather_parsed
    weather_parsed = json.loads(z_json_string)
    z.close()

    
    
def set_description():
    description = weather_parsed['current_observation']['weather']
    if description =="":
        description = uv_parsed['current_observation']['weather']
        if description =="":
            description = "Typisch zeeweertje :-) "
            return description
        else:
            return description + "; "
    else:
        return description + "; "


def set_temperature():
    temperature = weather_parsed['current_observation']['temp_c']
    return str(temperature) + "°C; "


def set_rain():
    hourly = pop_parsed['hourly_forecast']
    rain = hourly[0]['pop']
    return str(rain) + "% kans op neerslag; "


def set_wind():
    wind_dir1 = weather_parsed['current_observation']['wind_dir']
    wind_dir2 = uv_parsed['current_observation']['wind_dir']
    wind_gust_kph1 = weather_parsed['current_observation']['wind_gust_kph']
    wind_gust_kph2 = uv_parsed['current_observation']['wind_gust_kph']
    if int(float(wind_gust_kph1)) == 0:
        if int(float(wind_gust_kph2)) == 0:
            wind = "windstil"
        else:
            wind = "wind: " + str(wind_gust_kph2) + "km/h " + wind_dir2
    else:
        wind = "wind: " + str(wind_gust_kph1) + "km/h " + wind_dir1
    return wind


def set_uv():
    uv = uv_parsed['current_observation']['UV']
    if int(uv) < 4:
        return ""
    else:
        return "; UV-index:" + str(uv)


def set_message():
    hashtag = " #weer #dekust"
    message = str(set_description()) + str(set_temperature()) + str(set_rain()) + str(set_wind()) + str(set_uv()) + hashtag
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
    message = set_message()
    tweet_message(picture,message) 


def delete_picture():
    os.remove("wb.jpg")
    

meteo()

