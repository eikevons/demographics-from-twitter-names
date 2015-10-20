# -*- coding: utf-8 -*-
import sys
import config
import tweepy
from name_search import NameSearch


class TwitterFollowers(NameSearch):
    def __init__(self, path, con_secret, con_secret_key, token_key, token):
      super(TwitterFollowers, self).__init__(path)
      auth = tweepy.OAuthHandler(con_secret, con_secret_key)
      auth.set_access_token(token, token_key)

      self.t = tweepy.API(auth)

    def get_followers(self, screen_name):
      followers = []
      i = 0
      # If you increase the number of returned results, you will probably
      # have to deal with rate limits from Twitter.
      for user in tweepy.Cursor(self.t.followers, screen_name=screen_name, count=200).items():
        followers.append(user.name.split(" ")[0])
        i = i + 1
        if (i > 200):
          break

      return followers


if __name__ == "__main__":
    twitter_name = 'sevenval'
    tn = TwitterFollowers(sys.argv[1], config.con_secret, config.con_secret_key, config.token_key, config.token)
    follower_names = tn.get_followers(twitter_name)
    r = []
    for forename in follower_names:
      o = tn.search(forename)
      if o:
        r.append(o[-1]) # Get the name with highest probability

    with open('demographics_' + twitter_name + '.csv','w') as of:
        of.write('name;sex;age\n')
        for o in r:
          of.write(o['name'] + ';' + o['sex'] +';' + str( 2015 - o['year']) + '\n')
