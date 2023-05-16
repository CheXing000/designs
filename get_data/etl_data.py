import sqlalchemy
import re
import pandas as pd
from pymysql import Connect, connect

con = Connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')
cur = con.cursor()
sql = """select scenery,city from scenery_all"""
df = pd.read_sql(sql, con)
df['city'] = df['city'].str.strip()
df['image_name'] = df['scenery']+'.jpg'
con =connect(host='localhost',port=3306,user='root',password='123456',database='edu_design')
cur = con.cursor()
cur.executemany("insert into scenery (`scenery`,`city`,`image_name`) values(%s,%s,%s)", df.values.tolist())
con.commit()


sql = """select * from scenery_detail_copy"""
df = pd.read_sql(sql, con)
address_list = []
way_list = []
open_time_list = []
t_list = []
for i in df['scenery_other']:
    address_list.append(eval(i).get('地址：', ''))
    way_list.append(eval(i).get('到达方式：', ''))
    open_time_list.append(eval(i).get('开放时间：', ''))
    t_list.append(eval(i).get('门票：', ''))
df['scenery_address'] = address_list
df['scenery_way'] = way_list
df['scenery_open'] = open_time_list
df['scenery_menpiao'] = t_list
df.drop(columns=['scenery_other'], inplace=True)
df['scenery_other'] = ''
df = df[['scenery_name', 'scenery_detail', 'mark', 'rank', 'scenery_address', 'scenery_way', 'scenery_open',
         'scenery_menpiao', 'scenery_other']]

con = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')
cur = con.cursor()
cur.executemany(
    "insert into scenery_web (`scenery_name` ,`scenery_detail`,`mark` ,`rank` ,`scenery_address`,`scenery_way` ,`scenery_open`, `scenery_menpiao`,`scenery_other`) "
    "values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
    df.values.tolist())
con.commit()
print(1)

sql = """select city,many_people from scenery_all group by city, many_people"""
df = pd.read_sql(sql, con)
df['city'] = df['city'].str.strip()
df['image_name'] = df['city']+'.jpg'
df['many_people'] = df['many_people'].map(lambda x:int(x[:-3]))
con = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')
cur = con.cursor()
cur.executemany(
    "insert into hot_city (`city` ,`many_people`,`city_image`) values(%s,%s,%s)",
    df.values.tolist())
con.commit()
print(1)

sql = """select * from ways"""
df = pd.read_sql(sql,con)
df['start_time'] = df['start_time'].map(lambda x:x[5:-3])
df['see_people'] = df['see_people'].astype(int)
df = df[['scenerys' ,'start_time','days','see_people','is_on']]
con = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')
cur = con.cursor()
cur.executemany(
    "insert into all_way (`scenerys` ,`start_time`,`days`,`say_people`,`is_on`) values(%s,%s,%s,%s,%s)",
    df.values.tolist())
con.commit()
print(1)

sql = """select * from way_test"""
df = pd.read_sql(sql, con)
info = []
df['address'] = df['address'].map(lambda x:re.sub('[A-Za-z]','',str(x)))
for i, r in df.iterrows():
    if eval(r.day_info):
        for _dict in eval(r.day_info):
            _ = [r.address,_dict.get('scenery', ''), _dict.get('mark', ''), r.date, r.is_on]
            info.append(_)
    else:
        _ = ['', '', r.date, r.is_on]
        info.append(_)
dff = pd.DataFrame(columns=['scenery', 'mark', 'date', 'is_on'], data=info)
con = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')
cur = con.cursor()
cur.executemany(
    "insert into ways_info (`address` ,`date`,`is_on`) values(%s,%s,%s)",
    df[['address', 'date', 'is_on']].values.tolist())
cur.executemany(
    "insert into ways_scenery (`address`,`date` ,`scenery`,`mark`,`is_on`) values(%s,%s,%s,%s)",
    dff[['date', 'scenery', 'mark', 'is_on']].values.tolist())
con.commit()
print(1)
