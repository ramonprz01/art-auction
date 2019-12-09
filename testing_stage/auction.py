# -*- coding: utf-8 -*-
import scrapy


class AuctionSpider(scrapy.Spider):
    name = 'auction'
    allowed_domains = ['www.ifar.org/']
    start_urls = ['http://http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=/']

    def parse(self, response):
        pass
