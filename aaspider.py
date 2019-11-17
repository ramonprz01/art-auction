# -*- coding: utf-8 -*-
import scrapy


class AaspiderSpider(scrapy.Spider):
    name = 'aaspider'
    allowed_domains = ['ifar.org']
    start_urls = ['http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=']
    prefix = "http://www.ifar.org/"
    

    def start_requests(self):
        yield scrapy.Request(url = start_urls, callback = self.parse)
    
    def parse(self, response):
        self.log('I just scraped: ' + response.url)
        
        name = response.css('td.g_center_name > a::text').extract(),
        link = response.css('td.g_center_name > a::attr(href)').extract(),
        birth_year =  response.css('.g_center_birth_year').extract(),
        birth_place = response.css('.g_center_birth_place').extract(),
        death_year = response.css('.g_center_death_year').extract(),
        death_place = response.css('.g_center_death_place').extract()
        
        urls = response.css('td.g_center_name > a::attr(href)').extract()
        for url in urls:
            url = prefix.join(url)
            yield scrapy.Request(url=url, callback = self.parse_details)
            
    
    def parse_details(self, response):
        box_info = response.css('div#box_2_left ::text').extract()
        catalogues_links = response.css('.catalogue_title > a::attr(href)').extract()
        
        urls_2 = response.css('.catalogue_title > a::attr(href)').extract()
        for url in urls_2:
            url = prefix.join(url)
            yield scrapy.Request(url=url, callback = self.parse_details_dos)
            
    
    def parse_details_dos(self, response):
        yield {
            'column_names' : response.css('.book_title > dl > dt::text').extract(),
            'content' : response.css('.book_title > dl > dd::text').extract()
        }