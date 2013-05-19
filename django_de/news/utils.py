from django.conf import settings

import tweepy


def get_twitter_api():
    auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY,
                               settings.TWITTER_CONSUMER_SECRET)

    auth.set_access_token(settings.TWITTER_ACCESS_TOKEN_KEY,
                          settings.TWITTER_ACCESS_TOKEN_SECRET)

    return tweepy.API(auth)
