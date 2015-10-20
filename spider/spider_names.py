# -*- coding: utf-8 -*-
"""
Run with scapy crawl vornamen
"""

import scrapy
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class DmozSpider(scrapy.Spider):
    name = "vornamen"

    start_urls = ["http://www.beliebte-vornamen.de/jahrgang/j" + str(i) for i in range(1890, 2015)]
    years_with_names = {}

    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        year = int(response.url.split("/")[-1][-4:])


        names = []

        for pos, name in enumerate(response.xpath('//ol[1]/li/a/text()').extract()):
            names.append((name, pos, "female"))

        for pos, name in enumerate(response.xpath('//ol[2]/li/a/text()').extract()):
            names.append((name, pos, "male"))

        self.years_with_names[year] = names

    def spider_closed(self, spider):
        ofname = 'names_with_year_prob.csv.new'
        with open(ofname,'w') as of:
            of.write('name;position;sex;year\n') # python will convert \n to os.linesep
            for year in self.years_with_names:
                for (name, pos, sex) in self.years_with_names[year]:
                    of.write("{};{};{};{}\n".format(name.encode("utf-8"), pos, sex, year))
                    print name
            print "Written to", ofname
