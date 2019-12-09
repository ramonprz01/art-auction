# Web Crawling the International Foundatiion for Art Research Website

_Last updated: **07 December 2019**_

Created by **Ramon Perez**

## *Outline*

![alt text](https://www.memecreator.org/static/images/memes/4967563.jpg)

This is a tutorial on how to crawl and clean the International Foundation for Art Research website. Althought this example is specific to this site, the code can be leveraged to crawl other sites where a three-part crawl is needed. For example, the code can be used for crawling a website where one has a main webpage to crawl, a sub-link, and a sub-sub-link to follow for crawling and scraping websites recursively.

For this tutorial, we will be using Python version 3.7.3 and [Scrapy](https://scrapy.org/) version 1.7.3 and JupyterLab since it provides a neat environment for working with jupyter notebooks, plain python, and the command line. The are other fantastic IDEs and tools out there for crawling such as Atom, and Spider, or [selenium](https://selenium-python.readthedocs.io/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), respectively, that could be used for this task as well. If you decide to try one of these, please share your process with others.

1. **Introduction to Scrapy**
2. **Intro to our Crawler**
3. **Crawling Part 1**
4. **Crawling Part 2**
5. **Crawling Part 3**
6. **Crawling Part 4**
7. **Initializing our Spider**


### 1. Introduction to Scrapy

Scrapy is an open source Python package used for extracting data from the web in a fast and concice way. Its powerful and yet simple sintax makes scrapy the perfect tool for extracting data from a large number of websites with a few lines of code.

For a better user experience, Scrapy is best when used in combination with the command line although it works totally fine while only using jupyter notebooks.

To install scrapy using pip open up the command line and go to the folder where the files for this project will live at and then type:

```shell
$  pip install scrapy
```

To install scrapy using Anaconda open up the anaconda prompt with administrator rights and then type:

```shell
$  conda install -c conda-forge scrapy
```

In the next section we will explore every part of our crawler in detail and then show how to run it

https://miro.medium.com/max/1100/0*Bj_O1jRFzZjKxzi4.jpg
### 2. Intro to our Crawler

The first thing we want to do before crawling any website is to determine whether there are any restrictions we should be aware of. To do this we type the name of the main site of the website we will be scraping and add "/robots.txt"

To initiate a spider crawler using scrapy we can use the command:


```shell
$  scrapy genspider aaspider http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=
```

The "aa" stands art and artist, and the spider is for what we will be creating.

Generating the spider with the previous commands provides a blank canvas with the website we intend to start our crawler from. When you run the command, scrapy will generate the .py file we need for our crawler. When you open it in JupyterLab you will see the following lines.

```python
import scrapy


class AaspiderSpider(scrapy.Spider):
    name = 'aaspider'
    allowed_domains = ['http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author=']
    start_urls = [
                'http://www.ifar.org/catalogues_raisonnes.php?alpha=&searchtype=artist&published=1&inPrep=1&artist=&author='
                ]
```

Change the allowed_domains variable to show the main website of the site.
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


