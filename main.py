import databasecontrol
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import API
import telegramhandler

def twitterapi():

    print("Twitter api")

    bearer_token = "AAAAAAAAAAAAAAAAAAAAADj4lQEAAAAAbvbjREqMX2bag5aafE9eL8nSFMI%3Du8U4oLk08AYQEG5PW6vHqbMPOKn85tJAGz0RTKeZS2Ioa84UqX"
    _consumer_key = "zGZPERPx1b9ix3fOXbBPKW3hZ"
    _consumer_secret = "GLltMBIBH7SN5VQJqNM03firqXe8nFb9DMcT1o0qgTv3XAzwMl"
    _access_token = "1619230600191217666-AJDkN5RSIlMpCb1to9ntaVA2ThKGiw"
    _access_secret = "Z7O3M8KcqGYg01tvFhQeDMnqThS6WY6VcmWCWcUgxO6uc"
    _client_id = "T0tPbVdJUkxkWFJoVHFBTnYxdHo6MTpjaQ"
    _client_secret = "hahIQG7D1NPE2o9Rd9rVrlxsE01K6NR2M6kCWZoZXeQzVInLwi"


    api = tweepy.Client(consumer_key = _consumer_key, 
            consumer_secret = _consumer_secret,
            access_token = _access_token,
        access_token_secret = _access_secret)
    print(api)
    
    return api

def formMessage(_list):
    if bool(_list):
        message = "Trending accounts on CT: "

        for key in _list:
            try:
                if key not in accountList:
                    message = message + "\n" + key #vaihda tähän at merkki ennen keytä
            except:
                message = message + "\n" + key #vaihda tähän at merkki ennen keytä
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
 
    time.sleep(60)
    print("6")

