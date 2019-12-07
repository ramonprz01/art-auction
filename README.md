# Web Crawling the International Foundatiion for Art Research Website

Last updated: 07 December 2019

Created by Ramon Perez

## *Outline*

![alt text](https://www.memecreator.org/static/images/memes/4967563.jpg)

This is a tutorial on how to crawl and clean the International Foundation for Art Research website. Althought this example is specific to this site, the code can be leveraged to crawl other sites where a three-part crawl is needed. That is, for a website where one has a main webpage to crawl, a sub-link, and a sub-sub-link to follow and crawl recursively.

For this tutorial, we will be using Python version 3.7.3 and [Scrapy](https://scrapy.org/) version 1.7.3 in JupyterLab since it provides a neat framework for working with jupyter notebooks, plain python, and the command line. The are other fantastic IDEs and tools out there for crawling such as [selenium](https://selenium-python.readthedocs.io/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) that could be used for this task as well. If you decide to try one of these, please share your process with others.

1. **Introduction to Scrapy**
2. **Intro to our Crawler**








### 1. Introduction to Scrapy

Scrapy is an open source Python package used for extracting data from the web in a fast and concice way. Its powerful and yet simple sintax makes scrapy the perfect tool for extracting data from a large number of websites with a few lines of code.

For a better user experience, Scrapy is best when used in combination with the command line although it works totally fine when using jupyter notebooks only.

To install scrapy using pip open up the command line and go to the folder where the files for this project will live at and then type:

```shell
$  pip install scrapy
```

To install scrapy using conda open up the anaconda prompt with administrator rights and then type:

```shell
$  conda install -c conda-forge scrapy
```


https://miro.medium.com/max/1100/0*Bj_O1jRFzZjKxzi4.jpg
### 2. Intro to our Crawler


The lines of code below will crawl all three parts of the 

```python
import scrapy


class AaspiderSpider(scrapy.Spider):
    name = 'aaspider'
    allowed_domains = ['www.ifar.org']
    start_urls = [
                'http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author='
                ]
    
    
    def parse(self, response):
        
        yield {
            'name': response.css('td.g_center_name > a::text').extract(),
            'link': response.css('td.g_center_name > a::attr(href)').extract(),
            'birth_year': response.css('.g_center_birth_year').extract(),
            'birth_place': response.css('.g_center_birth_place').extract(),
            'death_year': response.css('.g_center_death_year').extract(),
            'death_place': response.css('.g_center_death_place').extract()
        }
        
        links_info = response.css('td.g_center_name > a::attr(href)')
        links = links_info.extract()
        href = []
        for url in links:
            href.append("http://www.ifar.org/" + url)

        for i in href:
            yield scrapy.Request(i, callback=self.parse_details) 
            
    
    def parse_details(self, response):
        
        yield {
            'artist_one' : response.css('h1::text').extract_first(),
            'box_info' : response.css('div#box_2_left ::text').extract()
            }
        
        
        new_info = response.css('.catalogue_title > a::attr(href)')
        new_links = new_info.extract()
        href_new = []
        for url_new in new_links:
            href_new.append("http://www.ifar.org/" + url_new)

        for s in href_new:
            yield scrapy.Request(s, callback=self.parse_details_dos)
        
     
    def parse_details_dos(self, response):

        yield {
            'artist_two' : response.css('h1::text').extract_first(),
            'column_names' : response.css('.book_title > dl > dt::text').extract(),
            'content' : response.css('.book_title > dl').css('dd').extract()
        }

```


