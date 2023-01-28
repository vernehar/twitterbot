import databasecontrol
import time
import tweepy
from tweepy import OAuthHandler
from tweepy import API

def twitterapi():

    print("Twitter api")

    bearer_token = "AAAAAAAAAAAAAAAAAAAAADj4lQEAAAAAbvbjREqMX2bag5aafE9eL8nSFMI%3Du8U4oLk08AYQEG5PW6vHqbMPOKn85tJAGz0RTKeZS2Ioa84UqX"
    _consumer_key = "zGZPERPx1b9ix3fOXbBPKW3hZ"
    _consumer_secret = "GLltMBIBH7SN5VQJqNM03firqXe8nFb9DMcT1o0qgTv3XAzwMl"
    _access_token = "1619230600191217666-UQLY0wx0nUFlEO6RpVhGLzqmJiLA2R"
    _access_secret = "hIDythEC9CPxLD7uFzAW4VzqO3LwNvdfjS8R3DxNxTywI"

    auth = tweepy.OAuthHandler(_consumer_key, _consumer_secret)
    auth.set_access_token(_access_token, _access_secret)
    api = tweepy.Client(consumer_key = _consumer_key, 
            consumer_secret = _consumer_secret,
            access_token = _access_token,
        access_token_secret = _access_secret)
    print(api)
    
    return api

def formMessage(_list):
    message = "Trending accounts on CT: "
    for key in _list:
        message = message + key + " "
        print(key)
    print(message)
    return message

        



api = twitterapi()
trendingAccounts = databasecontrol.trendingWithinTimePeriod(24)
message = formMessage(trendingAccounts)
response = api.create_tweet(text="gm")



time.sleep(15)

