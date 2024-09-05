import scrapy
from ..items import NflSalariesItem


class SalariesSpider(scrapy.Spider):
    name = "salaries"
    allowed_domains = ["www.spotrac.com"]
    start_urls = [
        "https://www.spotrac.com/nfl/cap/_/year/2023/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2022/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2021/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2020/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2019/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2018/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2017/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2016/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2015/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2014/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2013/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2012/sort/cap_total/dir/asc",
        "https://www.spotrac.com/nfl/cap/_/year/2011/sort/cap_total/dir/asc"
    ]

    def parse(self, response):
        items = NflSalariesItem()

        salary_cap_year = response.xpath('//select/option[@selected="selected"]/text()').extract()
        items['salary_cap_year'] = salary_cap_year

        for table in response.xpath('//table'):
            if len(table.xpath('//tbody//tr')) > 5:
                rows = table.xpath('//tbody/tr')
                break

        data = []

        for row in rows:
            try:
                team_abbreviation = row.xpath('.//td/span/text()').extract()
                team_salaries = row.xpath('.//td[position()>2]/text()').extract()
                combined_team_data = team_abbreviation + team_salaries
                team_data = [single_team.strip() for single_team in combined_team_data]

                items['team_abbreviation'] =  team_data[0]
                items['active_salaries'] = team_data[7]
                items['dead_money'] = team_data[9]
                items['total_cap'] = team_data[5]

                yield items
            except IndexError:
                pass
