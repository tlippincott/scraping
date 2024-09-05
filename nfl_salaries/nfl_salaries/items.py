# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NflSalariesItem(scrapy.Item):
    salary_cap_year = scrapy.Field()
    team_abbreviation = scrapy.Field()
    active_salaries = scrapy.Field()
    dead_money = scrapy.Field()
    total_cap = scrapy.Field()
