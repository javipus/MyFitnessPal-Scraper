from __future__ import print_function
from __future__ import division

import os, sys, time

import numpy as np
import pandas as pd

import urlparse

from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import HtmlXPathSelector
from myfitnesspal.items import MyfitnesspalItem

from bs4 import BeautifulSoup
import HTMLParser

# TODO: pass USERNAME to CrawlSpider
USERNAME = 'YOUR_USERNAME_GOES_HERE'

def getDiary(diaryHTML):

    # Return this dataframe
    df = []

    # TODO: extract date from html file name and pass it to dataframe
    date = diaryHTML.strip('.html').split('_')[-1]

    # Parse HTML
    with open(diaryHTML, 'r') as f:
        soup = BeautifulSoup(f)
    
    # Nutrition Table
    table = soup.find('table', {'class': 'table0'})
    
    # Get list of rows
    rows = table.find_all('tr')

    for i, row in enumerate(rows):

        if not i: # define table header
            nutrients = row.find_all('td', {'class': 'alt nutrient-column'})
            header = [n.text.strip().strip('\n').split()[0] for n in nutrients]
        
        else:
            if not row.attrs:
                
                food = row.find('td', {'class': 'first alt'})

                if food:
                    food = food.text.strip()
                else: # nothing to see here
                    continue
                
                if food[-1] == 'g': # quantity in grams
                    # 
                    # TODO:
                    # 
                    # Serving size is not codified in such a regular way
                    # because:
                    #
                    # 1. There are units other than grams (ml, teaspoons, etc)
                    # 2. 100 g == 100 grams
                    # 3. Not always comma separated
                    #
                    try:
                        quant = float(food.split(',')[-1].replace('g', ' ').strip())
                    except ValueError:
                        quant = 0
                else:
                    quant = 0

                # TODO: this only works if the table settings are such that:
                #
                #       cals | macro | micro | macro | macro | micro
                #       
                #       And of course the actual meaning of the vars will be
                #       different but that is accounted for by parsing the
                #       header
                
                carbs, fat, prot = row.find_all('span', {'class': 'macro-value'})
                
                cals = carbs.find_parent().find_previous_sibling()
                sugar = fat.find_parent().find_previous_sibling()
                fiber = carbs.find_parent().find_next_sibling()
                
                data = [date, food, quant] + map(lambda x: float(x.text.replace(',', '')), (cals, carbs, fat, prot, sugar, fiber))
                
                df.append(data)

            else:
                if row.attrs['class'][0] == 'meal_header':
                    # TODO: parse this to have time info
                    #       or maybe do it without else statement, just
                    #       looking for parents/siblings in the if above
                    continue


    df = pd.DataFrame(df, columns = ['Date', 'Food', 'Grams'] + header)

    return df

class MyfitnesspalSpider(CrawlSpider):
    """ General configuration of the Crawl Spider """

    name = 'Myfitnesspal'

    # urls from which the spider will start crawling
    allowed_domains = ['myfitnesspal.com']
    start_urls = ['http://www.myfitnesspal.com/food/diary/{}'.format(USERNAME)]
    crawlURLs = [r'\?date.*']
    
    myXPaths = '//a[contains(@class, "prev")]'
    myLinkExtractor = LinkExtractor(allow = crawlURLs, restrict_xpaths = myXPaths)

    rules = [Rule(myLinkExtractor, callback = 'parse_item', follow = True)]

    def parse_item(self, response):
        dataFolder = 'data'
        filename = 'mfp_diary_{}.html'.format(response.url.split('date=')[-1])
        filePath = '/'.join([dataFolder, filename])

        if os.path.isfile(filePath):
            print('\n{} already in database!'.format(filePath))
            return
        else:
            print('\nParsing... {}'.format(response.url))
            with open(filePath, 'w') as f:
                f.write(response.body)
        
            time.sleep(1. + max([np.random.randn(1), -1]))
