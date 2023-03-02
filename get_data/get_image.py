import parsel
import requests
import re
import os
import time
import sqlalchemy
import pandas as pd


class GetImg(object):
    def __init__(self):
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_qyeruid=CgIBAWNM7YyZ0xpWP191Ag==; new_uv=1; new_session=1; _guid=Rb9104db-c9f6-e034-0cad-4e9bc2b2a446; __utma=253397513.301964923.1665985935.1665985935.1665985935.1; __utmc=253397513; __utmz=253397513.1665985935.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ql_guid=QL032b7b-b194-42de-92cf-163a7dab7397; ql_created_session=1; ql_stt=1665985934546; ql_vts=1; frombaidu=1; PHPSESSID=a55004d0275f0b5c5e67dac784e3ad04; isnew=1665985978678; source_url=https%3A//place.qyer.com/; isDoLogin=828; city_browse=a%3A1%3A%7Bi%3A0%3Bi%3A11595%3B%7D; __utmb=253397513.9.10.1665985935; ql_seq=9',
            'referer': 'https://place.qyer.com/china/citylist-0-0-1/'}
        self.con = sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost:3306/edu_design?charset=utf8")

    def api_image(self, url):
        res = requests.get(url, self.header)
        return res.text

    def save_image(self, city_name, url):
        path = r'G:\\image\\'
        if not os.path.exists(path):
            os.makedirs(path)
        img_data = requests.get(url, self.header).content
        with open(path + city_name + '.jpg', 'wb') as f:
            f.write(img_data)
            f.close()
            print(city_name + '图片保存完成')
            time.sleep(1)

    def save_scenery_img(self, scenery_name, url):
        path = r'G:\\scenery_img\\'
        if not os.path.exists(path):
            os.makedirs(path)
        img_data = requests.get(url, self.header).content
        with open(path + scenery_name + '.jpg', 'wb') as f:
            f.write(img_data)
            f.close()
            print(scenery_name + '图片保存完成')
            time.sleep(1)

    def get_scenery_img(self, img_html, img_name):
        data = parsel.Selector(img_html)
        data_list = data.xpath('.//div[@class="poi-placeinfo clearfix"]/a/p').getall()
        view_url = re.findall('src="(.*?)"', str(data_list))
        try:
            self.save_scenery_img(img_name, view_url[0])
        except:
            pass
        time.sleep(1)

    def get_scenery_image(self, url, scenery_name):
        j = 0
        for i in url:
            _url = 'https:' + i
            scenery_html = self.api_image(_url)
            self.get_scenery_img(scenery_html, scenery_name[j])
            j = j + 1

    def get_image_url(self, city_html):
        par = parsel.Selector(city_html)
        url_list = par.xpath('.//ul[@class="plcCitylist"]/li')
        for i in url_list:
            view = i.xpath('.//p[@class="pois"]/a/text()').getall()
            view_name = [i.strip() for i in view]
            view_urlall = i.xpath('.//p[@class="pois"]/a').getall()
            view_url = re.findall('href="(.*?)"', str(view_urlall))
            self.get_scenery_image(view_url, view_name)
            # text = i.xpath('.//p/a/img').get()
            # palce = i.xpath('.//h3/a/text()').get()
            # palce = palce.split()[0]
            # url = re.findall('src="(.*?)"',text)[0]
            # self.save_image(palce,url)

    def res_main(self):
        for i in range(13, 14):
            url = 'https://place.qyer.com/china/citylist-0-0-{page}/'.format(page=i)
            city_html = self.api_image(url)
            city_df = self.get_image_url(city_html)
            print("第%d页爬取完成" % i)


if __name__ == '__main__':
    a = GetImg()
    a.res_main()
