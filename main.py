import databasecontrol
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import API
import telegramhandler
import os

def twitterapi():

    print("Twitter api")


    api = tweepy.Client(consumer_key = os.environ["CONSUMER_KEY"], 
            consumer_secret = os.environ["CONSUMER_SECRET"],
            access_token = os.environ["ACCESS_TOKEN"],
        access_token_secret = os.environ["ACCESS_SECRET"])
    print(api)
    
    return api

def formMessage(_list):
    if bool(_list):
        message = "Trending accounts on CT: "

        for key in _list:
            try:
                if key not in accountList:
                    print("not in")
                    message = message + "\n" +"@"+key 
            except:
                print("except")
                message = message + "\n" +"@"+key 
        message = message + "\n" + "\n" + telegramhandler.getSponsorMessage()
    else:
        message = ""

    accountList = []
    for key in _list:
        accountList.append(key)

    return message

while True:
    print("1")
    api = twitterapi()
    print("2")
    trendingAccounts = databasecontrol.trendingWithinTimePeriod(48)
    print("3")
    message = formMessage(trendingAccounts)
    print("4")
    if message != "":
        try:
            response = api.create_tweet(text=message)
        except:
            print("post unsuccesful")
    else:
        print("no new accounts to post")
    print("5")
 
    time.sleep(14400)
    print("6")

