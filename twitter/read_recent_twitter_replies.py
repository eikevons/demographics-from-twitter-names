# -*- coding: utf-8 -*-
import sys
import config
from twitter import Twitter, OAuth
from name_search import NameSearch


class TwitterNotifications(NameSearch):
    def __init__(self, path, con_secret, con_secret_key, token_key, token):
        super(TwitterNotifications, self).__init__(path)
        self.t = Twitter(auth=OAuth(token, token_key, con_secret, con_secret_key))

    def get_twitter_names(self):
        data = self.t.statuses.mentions_timeline(count=10)
        for reply in data:
            n = reply['user']['name'].split(" ")[0]
            r = self.search(n)
            if r:
                yield n, r[-1]


if __name__ == "__main__":
    tn = TwitterNotifications(sys.argv[1], config.con_secret, config.con_secret_key, config.token_key, config.token)
    with open('demographics_replies.csv', 'w') as of:
        of.write('name;sex;age\n')
        for name, o in tn.get_twitter_names():
            of.write(o['name'] + ';' + o['sex'] +';' + str( 2015 - o['year']) + '\n')
            print "{}: {}".format(name, o)
