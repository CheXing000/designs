import time

from pymysql import Connect, connect
import pandas as pd
import numpy as np
import datetime

con = Connect(host='localhost', port=3306, user='root', password='123456', database='edu_design', charset='utf8')
conn = connect(host='localhost', port=3306, user='root', password='123456', database='edu_design', charset='utf8')


def people_data(username):
    sql = """ select username,email,is_active,is_staff from auth_user where username='{username}'""".format(
        username=username)
    df = pd.read_sql(sql, con)
    return dict(zip(df.columns.tolist(), df.values.tolist()[0]))


def get_hot_city():
    sql = """select city,many_people,city_image from hot_city order by many_people desc limit 30"""
    df = pd.read_sql(sql, con)
    city_dict = dict(zip(df['city'].tolist(), df['city'].tolist()))
    df['many_key'] = df['city'] + '_m'
    many_dict = dict(zip(df['many_key'].tolist(), df['many_people'].tolist()))
    df['img_key'] = df['city'] + '_img'
    img_dict = dict(zip(df['img_key'].tolist(), df['city_image'].tolist()))
    city_dict.update(many_dict)
    city_dict.update(img_dict)
    return city_dict


def get_way_info(is_on):
    sql = """ select * from way_info where is_on={}""".format(is_on)
    df = pd.read_sql(sql, con)
    if df.empty:
        return []
    arg_list = []
    for i, r in df.iterrows():
        arg_dict = {}
        arg_dict['address'] = r.address
        arg_dict['date'] = r.date
        a = 1
        for j in eval(r.day_info):
            arg_dict['scenery_{}'.format(a)] = j.get('scenery', '')
            arg_dict['mark_{}'.format(a)] = j.get('mark', '')
            a = a + 1
        arg_list.append(arg_dict)
    return arg_list


def get_scenery_info(scenery_name):
    sql = """SELECT scenery_web.scenery_name, `scenery_web`.mark,`scenery`.city,`scenery`.image_name FROM `scenery_web` 
     JOIN scenery on scenery_web.scenery_name=scenery.scenery where scenery_name='{}'""".format(scenery_name)
    df = pd.read_sql(sql, con)
    if df.empty:
        return {}
    return {'mark': df.mark.values.tolist()[0], 'city': df.city.values.tolist()[0],
            'image_name': df.image_name.values.tolist()[0]}


def save_way(value_list):
    sql = """insert into user_way (`city`,`date`,`mark`,`user`,`scenery`,`say_people`,is_web,`image_name`) values 
    (%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur = conn.cursor()
    cur.executemany(sql, [value_list])
    conn.commit()


def get_date(df):
    arg_list = []
    date = df.drop_duplicates(subset=['date'])['date'].tolist()
    dff = df.groupby(['date'])
    for i in date:
        arg = {}
        city = dff.get_group(i).drop_duplicates(subset=['city'])['city'].tolist()
        arg['city'] = '&'.join(city)
        arg['date'] = i
        arg_list.append(arg)
    return arg_list


def update_way_status(user, df):
    status = False
    sql = """SELECT id,city,date,scenery,mark,say_people,image_name from user_way WHERE `user` = '{user}' and is_web='0' ORDER BY create_time""".format(
        user=user)
    sql1 = """select is_on from all_way"""
    if df.empty:
        df = pd.read_sql(sql, con)
    df = df[['id', 'city', 'date', 'scenery', 'mark', 'say_people','image_name']]
    if df.empty:
        return False, 0
    dff1 = pd.read_sql(sql1, con)
    df1 = pd.DataFrame({"is_on":dff1.astype(int).is_on.max()},index=[0])
    df1['scenerys'] = '~'.join(df.drop_duplicates(subset=['city']).city.values.tolist())
    dates = [min(df.drop_duplicates(subset=['date']).date.values.tolist()),
             max(df.drop_duplicates(subset=['date']).date.values.tolist())]
    df1['days'] = (pd.to_datetime(dates[1]) - pd.to_datetime(dates[0])).days + 1
    df1['is_on'] = df1['is_on'].astype(int) + 1
    df1['see_people'] = 1
    df1['start_time'] = min(df.drop_duplicates(subset=['date']).date.values.tolist())
    df1['create_time'] = datetime.datetime.now()
    df1.rename(columns={'see_people':'say_people'},inplace=True)
    in_ways = """insert into all_way({columns}) values (%s,%s,%s,%s,%s,%s)""".format(
        columns=','.join(df1.columns.tolist()))
    df2 = df[['city', 'date']]
    df2['is_on'] = df1.is_on.values.tolist()[0]
    df2.drop_duplicates(subset=['date'],keep='first',inplace=True)
    df2.rename(columns={'city': 'address'}, inplace=True)
    in_way_info = """insert into ways_info ({columns}) values(%s,%s,%s)""".format(
        columns=','.join(df2.columns.tolist()))
    df3 = df[['date', 'scenery', 'mark', 'image_name']]
    df3['is_on'] = df1.is_on.values.tolist()[0]
    df3['image_name'] = 'page_image/scenery_image/'+df3['image_name']
    in_way_scenery = """insert into ways_scenery({columns})values (%s,%s,%s,%s,%s)""".format(
        columns=','.join(df3.columns.tolist()))
    df4 = df[['id']]
    df4['is_web'] = '1'
    update_sql = """update user_way set is_web=(%s) where id=(%s)"""
    df5 = df1.copy()
    df5['end_time'] = max(df.drop_duplicates(subset=['date']).date.values.tolist())
    df5.rename(columns={'see_people': 'say_people'}, inplace=True)
    df5['user'] = str(user)
    df5 = df5[['scenerys', 'start_time', 'end_time', 'days', 'say_people', 'is_on', 'user']]
    in_user_detil = """insert into user_way_detail({columns})values (%s,%s,%s,%s,%s,%s,%s)""".format(
        columns=','.join(df5.columns.tolist()))
    cursor = conn.cursor()
    cursor.execute('SET autocommit = 0')
    try:
        cursor.executemany(in_way_scenery, df3.values.tolist())
        cursor.executemany(update_sql, df4[['is_web', 'id']].values.tolist())
        cursor.executemany(in_ways, df1.values.tolist())
        cursor.executemany(in_way_info, df2.values.tolist())
        cursor.executemany(in_user_detil, df5.values.tolist())
        status = True
    except:
        conn.rollback()
    finally:
        conn.commit()
    return status, df1.is_on.tolist()[0]


# update_way_status('chexing')


def get_add(is_on):
    sql = """
SELECT ways_scenery.scenery,scenery_adds.location,ways_scenery.is_on from ways_scenery 
join scenery_adds on ways_scenery.scenery like scenery_adds.scenery where ways_scenery.is_on = '{is_on}' """.format(is_on=is_on)
    add_df = pd.read_sql(sql, conn)
    if add_df.empty:
        return {'error':'路线景区经纬度未保存到数据库中'}
    add_df[['location_1', 'location_2']] = add_df['location'].str.split(',', 1, expand=True)
    return add_df[['location_1', 'location_2']].dropna().astype(float).to_numpy()


def get_way_name(is_on):
    sql = """SELECT scenerys,days from all_way where is_on='{is_on}'""".format(is_on=is_on)
    df = pd.read_sql(sql, conn)
    return df
