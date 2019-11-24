# -*- coding: utf-8 -*-
import scrapy


class AuctionSpider(scrapy.Spider):
    name = 'auction'
    allowed_domains = ['http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=']
    start_urls = ['http://http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=/']

    def parse(self, response):
        pass
