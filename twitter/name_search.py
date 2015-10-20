# -*- coding: utf-8 -*-
from __future__ import division
import csv

class NameSearch(object):
    def __init__(self, path):
        self.names = []
        with open(path, "rb") as csvfile:
            for row in csv.reader(csvfile, delimiter=';'):
                o = {'name': row[0].decode("utf-8"),
                     'sex': row[2]
                    }

                try:
                    o['prob'] = float(row[1])
                except ValueError as e:
                    print "Failed to parse probability: {}".format(e)

                try:
                    o['year'] = int(row[3])
                except ValueError as e:
                    print "Failed to parse year: {}".format(e)

                self.names.append(o)


    def demography_weight(self, name_data):
        central_year = 1980
        lower_halftime = 30
        upper_halftime = 20
        position_bonus_bound = 10

        position = name_data['position']
        if position < position_bonus_bound:
            pos_weight = (position_bonus_bound - position) / position_bonus_bound
        else:
            pos_weight = 1

        year = name_data['year']
        if year < central_year:
            age_weight = 0.5**((central_year - year) / lower_halftime)
        elif year < central_year:
            age_weight = 0.5**((year - central_year) / upper_halftime)
        else:
            age_weight = 1

        return age_weight * pos_weight


    def search(self, name):
        res = (i for i in self.names if name in i["name"])
        return sorted(res, key=lambda i: i.get("prob", 0))
