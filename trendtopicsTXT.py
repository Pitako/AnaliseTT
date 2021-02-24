#!/usr/bin/env python
#coding: utf-8

# In[2]:


import sys
import tweepy
import json
from datetime import datetime

#import mysql.connector
import time
import pytz


#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

# In[3]:


#Autenticacoes
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''


# In[4]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
 
# O Yahoo! Where On Earth ID para o Brasil e 23424768.
# Veja mais em https://dev.twitter.com/docs/api/1.1/get/trends/place e http://developer.yahoo.com/geo/geoplanet/
BRAZIL_WOE_ID = 23424768
 

outputFile = 'trendtopicsUTC.txt'


# In[23]:

tz = pytz.timezone('UTC')

while True:    
    now = datetime.now(tz)
    if ( int(now.strftime('%M'))%5==0.0 ):
        try:
            brazil_trends = api.trends_place(BRAZIL_WOE_ID) 
            trends = json.loads(json.dumps(brazil_trends, indent=1))

            for trend in trends[0]["trends"]:
                #print (trend["name"]+' '+str(trend["tweet_volume"]))                            
                val = now.strftime("%d/%m/%Y %H:%M:%S") + ";" + trend["name"] + ";" + str(trend["tweet_volume"]) + '\n';
                                               
                file = open(outputFile, mode='at+', newline=None, encoding='utf-8')
                #print(val)                
                
                file.write(val)
                file.close()

            #print (now.strftime("%d/%m/%Y %H:%M:%S"))            
            time.sleep(65)
        except Exception as e:
            print (now.strftime("%d/%m/%Y %H:%M:%S"))
            print(e)
            print()
            time.sleep(20)
            continue
            

        





