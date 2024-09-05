# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NflSalariesPipeline:
    def __init__(self) -> None:
        self.create_connection()

    def create_connection(self):
        self.conn = sqlite3.connect('/Users/terrylippincott/nfl_salaries.db')
        self.db_cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.db_cursor.execute("""
            SELECT id
            FROM   Teams
            WHERE  team_abbreviation = ?                          
        """, (item['team_abbreviation'],))

        team_id = self.db_cursor.fetchone()[0]

        data_year = int(item['salary_cap_year'][0])

        active_salaries_string = item['active_salaries']
        dead_money_string = item['dead_money']
        total_cap_string = item['total_cap']

        active_salaries_num = active_salaries_string.replace('$', '').replace(',', '')
        dead_money_num = dead_money_string.replace('$', '').replace(',', '')
        total_cap_num = total_cap_string.replace('$', '').replace(',', '')

        active_salaries = -1 if active_salaries_num == None else int(active_salaries_num)
        dead_money = -1 if dead_money_num == None else int(dead_money_num)
        total_cap = -1 if total_cap_num == None else int(total_cap_num)

        self.store_data(data_year, team_id, active_salaries, dead_money, total_cap)
        return item
    
    def store_data(self, data_year, team_id, active_salaries, dead_money, total_cap):
        self.db_cursor.execute("""
            INSERT INTO Salaries (year, team_id, active_salaries, dead_money, total_cap)
            VALUES (?, ?, ?, ?, ?)
        """,(data_year, team_id, active_salaries, dead_money, total_cap))

        self.conn.commit()