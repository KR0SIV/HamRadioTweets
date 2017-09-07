#!/usr/bin/env python
from twython import Twython
import aprslib
from configparser import ConfigParser as config

config.read('key.txt')
APP_KEY = config.get('Twitter', 'APP_KEY')
APP_SECRET = config.get('Twitter', 'APP_SECRET')
OAUTH_TOKEN = config.get('Twitter', 'OAUTH_TOKEN')
OAUTH_TOKEN_SECRET = config.get('Twitter', 'OAUTH_TOKEN_SECRET')
call = config.get('APRS', 'call')
passwd = config.get('APRS', 'pass')


twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

import aprslib
import re

def start():
    aprs = aprslib.IS(call, passwd=passwd)
    aprs.connect()
    # send a packet
    #aprs.sendall("TWITR>APRS,TCPIP*:>Python HamRadioTweets Server Started")
    #tweet('Python Dev Server Started')
    aprs.consumer(parse, raw=True)

def parse(packet):
    spack = str(packet)
    regexp = re.compile('TWITR') #change callsign
    if regexp.search(spack):
        strip1 = re.sub(r'>.+TWITR\s+:', ':', spack) #change callsign
        strip2 = re.sub(r'b.', '', strip1)
        msg = re.sub(r'.\Z', '', strip2)
        tweet(msg) #Tweet immediately after parsing
    else:
        pass

def tweet(status):
    twitter.update_status(status=status)


start()