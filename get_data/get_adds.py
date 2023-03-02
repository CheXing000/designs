import pandas as pd
from pymysql import Connect, connect
import requests


class GetAdd(object):

    def __init__(self):
        self.con = Connect(host='localhost', port=3306, user='root', password='123456', database='edu_design',
                           charset='utf8')
        self.AK = '543b057f8c6641e4ae48d6e5af68c03a'

    def get_scenery(self):

        sql = """select scenery,city from scenery"""
        df = pd.read_sql(sql, self.con)
        return df

    def get_lng(self, address):
        url = 'https://restapi.amap.com/v3/geocode/geo?address={}&output=json&key={}'.format(address, self.AK)
        print(url)
        res = requests.get(url)
        res = res.text
        try:
            location = eval(res).get('geocodes')[0].get('location')
        except:
            location = ''
        return location

    def to_db(self, df):
        conn = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design',
                       charset='utf8')
        sql = """insert into scenery_adds ({columns}) values (%s,%s,%s) """.format(
            columns=','.join(df.columns.tolist()))
        cur = conn.cursor()
        cur.execute('SET autocommit = 0')
        try:
            cur.executemany(sql, df.values.tolist())
        except:
            conn.rollback()
        finally:
            conn.commit()
        print('写入完成')

    def get_adds(self, add_df):
        location_list = []
        for i, r in add_df.iterrows():
            location = self.get_lng(r.city + r.scenery)
            location_list.append(location)
        add_df['location'] = location_list
        self.to_db(add_df)

    def main(self):
        add_df = self.get_scenery()
        self.get_adds(add_df)


if __name__ == '__main__':
    GetAdd().main()
