# -*- coding: utf-8 -*-
import time
import requests
import parsel
import re
import os
import sqlalchemy
import pandas as pd
import random


class GetWay(object):

    def __init__(self):
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_qyeruid=CgIBAWNM7YyZ0xpWP191Ag==; new_uv=1; new_session=1; _guid=Rb9104db-c9f6-e034-0cad-4e9bc2b2a446; __utma=253397513.301964923.1665985935.1665985935.1665985935.1; __utmc=253397513; __utmz=253397513.1665985935.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ql_guid=QL032b7b-b194-42de-92cf-163a7dab7397; ql_created_session=1; ql_stt=1665985934546; ql_vts=1; frombaidu=1; PHPSESSID=a55004d0275f0b5c5e67dac784e3ad04; isnew=1665985978678; source_url=https%3A//place.qyer.com/; isDoLogin=828; city_browse=a%3A1%3A%7Bi%3A0%3Bi%3A11595%3B%7D; __utmb=253397513.9.10.1665985935; ql_seq=9',
            'referer': 'https://place.qyer.com/china/citylist-0-0-1/'}
        self.con = sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost:3306/edu_design?charset=utf8")
        self.path = r'G:\way_image\\'

    def get_api(self, url):
        html_info = requests.get(url, self.header)
        return html_info.text

    def df_to_sql(self, df, table_name):
        df.to_sql(name=table_name, con=self.con, if_exists='append', index=False)

    def save_img(self, url, path, image_name):
        image_path = self.path + "\\" + path
        image_data = requests.get(url, self.header).content
        if os.path.isdir(image_path) == False:
            os.makedirs(image_path)
        with open(image_path + "\\" + image_name + ".jpg", 'wb') as f:
            f.write(image_data)
            f.close()

    def get_way_info(self, url, is_on):
        url = 'https:' + url
        way_lists = []
        way_info = self.get_api(url)
        way_info = parsel.Selector(way_info)
        days_items = way_info.xpath('.//section/div[@class="day"]')
        for days in days_items:
            way_list = []
            scenery_info = days.xpath('.//article[@class="poi clearfix"]')
            address = days.xpath('.//div[@class="vm-inner"]/h4/a/text()').get()
            dates = days.xpath('.//div[@class="vm-inner"]/h3/text()').get()
            if address:
                way_list.append("".join(address.split()))
            else:
                way_list.append(address)
            way_list.append(dates)
            scenery_list = []
            for info in scenery_info:
                scenert_dict = {}
                scenert_dict['scenery'] = info.xpath('.//section/h5/a/text()').get()
                if not scenert_dict['scenery']:
                    scenert_dict['scenery'] = info.xpath('.//section/h5/span/text()').get()
                    scenert_dict['scenery'] = "".join(scenert_dict['scenery'].split())
                    scenert_dict['mark'] = ''
                else:
                    scenert_dict['scenery'] = "".join(scenert_dict['scenery'].split())
                    scenert_dict['mark'] = info.xpath('.//section/p/span/text()').get()
                scenery_list.append(scenert_dict)
            way_list.append(str(scenery_list))
            way_lists.append(way_list)
        df = pd.DataFrame(columns=['address', 'date', 'day_info'], data=way_lists)
        df['is_on'] = is_on
        self.df_to_sql(df, 'way_info')

    def etl_html_info(self, html_info,is_on):
        way_lists = []
        html_info = parsel.Selector(html_info)
        items_list = html_info.xpath('.//div[@class="list"]/div')
        for item in items_list:
            way_list = []
            item_info = item.xpath('.//a')[0]
            days = item_info.xpath('.//div[@class="day"]/strong/text()').get()
            start_time = item_info.xpath('.//dl[@class="fontYaHei"]/dt/text()').get()
            scenerys = item_info.xpath('.//div[@class="plan"]/p/text()').get()
            see_people = item_info.xpath('.//div[@class="number"]/span/text()').get()
            img_url = item_info.xpath('.//div[@class="img"]').get()
            img_url = re.findall('data-original="(.*?)"', img_url)[0]
            info_url = item.xpath('.//a').get()
            item_url = re.findall('href="(.*?)"', info_url)
            self.save_img(img_url, 'scenery_way_img', str(is_on))
            if int(days) <= 5:
                self.get_way_info(item_url[0], is_on)
            way_list.append(scenerys)
            way_list.append(days)
            way_list.append(start_time)
            way_list.append(see_people)
            way_list.append(is_on)
            way_lists.append(way_list)
            is_on = is_on+1
        df = pd.DataFrame(columns=['scenerys', 'days', 'start_time', 'see_people', 'is_on'], data=way_lists)
        self.df_to_sql(df, 'ways')
        return is_on

    def get_main(self):
        url = "https://plan.qyer.com/search_0_0_11_0_0_0_{}/"
        is_on =1
        for page in range(1, 201):
            html_info = self.get_api(url.format(page))
            is_on = self.etl_html_info(html_info,is_on)
            time.sleep(1)
            print('第{}页爬取完成'.format(page))


if __name__ == '__main__':
    a = GetWay()
    a.get_main()
    # url = 'https://plan.qyer.com/trip/V2UJYVFnBzZTbFI4Cm8NPQ/'
    # a.get_way_info(url,is_on=5)
