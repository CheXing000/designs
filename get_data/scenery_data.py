import parsel
import requests
import re
import os
import time
import sqlalchemy
import pandas as pd


class GetData(object):
    def __init__(self):
        self.header = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_qyeruid=CgIBAWNM7YyZ0xpWP191Ag==; new_uv=1; new_session=1; _guid=Rb9104db-c9f6-e034-0cad-4e9bc2b2a446; __utma=253397513.301964923.1665985935.1665985935.1665985935.1; __utmc=253397513; __utmz=253397513.1665985935.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; ql_guid=QL032b7b-b194-42de-92cf-163a7dab7397; ql_created_session=1; ql_stt=1665985934546; ql_vts=1; frombaidu=1; PHPSESSID=a55004d0275f0b5c5e67dac784e3ad04; isnew=1665985978678; source_url=https%3A//place.qyer.com/; isDoLogin=828; city_browse=a%3A1%3A%7Bi%3A0%3Bi%3A11595%3B%7D; __utmb=253397513.9.10.1665985935; ql_seq=9',
            'referer': 'https://place.qyer.com/china/citylist-0-0-1/'}
        self.con = sqlalchemy.create_engine("mysql+pymysql://root:123456@localhost:3306/edu_design?charset=utf8")
        self.path = r'D:\image\\'

    def get_data(self, url):
        res = requests.get(url, self.header)
        return res.text

    def data_to_db(self, frame, table_name):
        frame.to_sql(name=table_name, con=self.con, if_exists='append', index=False)

    def save_img(self, id, scenery_name, city):
        url = 'https://place.qyer.com/images.php?action=list&id={id}&type=poi&offset=0&limit=30'.format(id=id[0])
        res = requests.get(url, self.header)
        html_data = res.text
        html_dict = eval(html_data)
        url_list = html_dict.get('data')['list']
        j = 1
        for i in url_list:
            url = i.get('url')
            url = url.replace('\\', '') + '?imageView/1/w/360/h/360/q/85/format/JPG'
            image_data = requests.get(url, self.header).content
            image_path = self.path + city + '\\' + scenery_name
            image_name = image_path + '\\' + str(j) + '.jpg'
            if os.path.isdir(image_path) == False:
                os.makedirs(image_path)
            with open(image_name, 'wb') as f:
                f.write(image_data)
                f.close()
            if j==10:
                break
            j = j + 1
        print(scenery_name + '：保存完毕')

    def get_img(self, url_df, city):
        for i, r in url_df.iterrows():
            if r.photo_url=='-':
                continue
            else:
                url = 'https:' + r.photo_url
                photo_html = self.get_data(url)
                _id = parsel.Selector(photo_html)
                _id = _id.xpath('.//div[@class="pla_photostop"]/p').get()
                id = re.findall('data-id="(.*?)"', _id)
                self.save_img(id, r.scenery_name, city)
                time.sleep(1)

    def get_scenery_dict(self,view_url,scenery_detail,data_dict,number,paiming):
        scenery_dict={}
        if view_url:
            scenery_dict['photo_url']=view_url
        else:
            scenery_dict['photo_url'] = '-'
        if scenery_detail:
            scenery_dict['scenery_detail']=scenery_detail
        else:
            scenery_dict['scenery_detail'] = '-'
        if data_dict:
            scenery_dict['scenery_other'] = data_dict
        else:
            scenery_dict['scenery_other']='-'
        if number:
            scenery_dict['mark']=number
        else:
            scenery_dict['mark'] = '-'
        if paiming:
            scenery_dict['rank'] = paiming
        else:
            scenery_dict['rank']='-'
        return scenery_dict
    def get_scenery_info(self, scenery_html):
        data = parsel.Selector(scenery_html)
        data_list = data.xpath('.//div[@class="poi-placeinfo clearfix"]/a').getall()
        view_url = re.findall('href="(.*?)"', str(data_list))
        data_boby = data.xpath('.//div[@class="compo-main"]')
        scenery_detail = data_boby.xpath('.//div[@class="poi-detail"]/div/p/text()').getall()
        scenery_detail = ','.join(scenery_detail)
        scenery_detail = scenery_detail.replace('\n', '')
        data_ul = data_boby.xpath('.//ul[@class="poi-tips"]/li/div/p/text()').getall()
        data_ull = data_boby.xpath('.//ul[@class="poi-tips"]/li/span/text()').getall()
        data_ulll = data_boby.xpath('.//ul[@class="poi-tips"]/li/div/a/text()').getall()
        data_ull = [i.strip() for i in data_ull]
        p = data_boby.xpath('.//div[@class="infos"]')
        p1 = data_boby.xpath('.//p[@class="points"]/span/text()').getall()
        number = ''.join([i.strip() for i in p1])
        paiming = p.xpath('.//ul/li/text()').getall() + [(p.xpath('.//ul/li/span/text()').getall())[-1]]
        paiming = ' '.join([i.strip() for i in paiming])
        if len(data_ull) == len(data_ul + data_ulll):
            data_dict = dict(zip(data_ull, data_ul + data_ulll))
        else:
            data_dict = dict(zip(data_ull[:len(data_ul)], data_ul))
        scenery_dict = self.get_scenery_dict(view_url,scenery_detail,[str(data_dict)],number,paiming)
        scenery_df = pd.DataFrame(scenery_dict)
        return scenery_df

    def etl_scenery_html(self, view_url, view_name, city):
        j = 0
        list_df = []
        for url in view_url:
            url = 'https:' + url
            scenery_html = self.get_data(url)
            scenery_df = self.get_scenery_info(scenery_html)
            scenery_df['scenery_name'] = view_name[j]
            scenery_df['city'] = city
            self.get_img(scenery_df[['photo_url', 'scenery_name']], city)
            j += 1
            list_df.append(scenery_df)
        try:
            df = pd.concat(list_df)
        except:
            df = pd.DataFrame()
        self.data_to_db(df, 'scenery_detail')
        print(city+'爬取完成')

    def etl_city_html(self, city_html):
        data = parsel.Selector(city_html)
        data_list = data.xpath('.//ul[@class="plcCitylist"]/li')
        df_list = []
        for i in data_list:
            palce = i.xpath('.//h3/a/text()').get()
            people = i.xpath('.//p[@class="beento"]/text()').get()
            view = i.xpath('.//p[@class="pois"]/a/text()').getall()
            view_name = [i.strip() for i in view]
            view_urlall = i.xpath('.//p[@class="pois"]/a').getall()
            view_url = re.findall('href="(.*?)"', str(view_urlall))
            self.etl_scenery_html(view_url, view_name, palce)
            df = pd.DataFrame({'scenery': view_name, 'view_url': view_url})
            df['city'] = palce
            df['many_people'] = people
            df_list.append(df)
        df = pd.concat(df_list)
        return df

    def get_info(self):
        for i in range(13, 50):
            url = 'https://place.qyer.com/china/citylist-0-0-{page}/'.format(page=i)
            city_html = self.get_data(url)
            city_df = self.etl_city_html(city_html)
            self.data_to_db(city_df, 'scenery_all')
            print("第%d页爬取完成")


if __name__ == '__main__':
    a = GetData()
    a.get_info()