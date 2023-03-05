# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BooksToScrapeItem(scrapy.Item):
    title = scrapy.Field()
    product_description = scrapy.Field()
    url = scrapy.Field()
