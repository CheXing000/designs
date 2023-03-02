import pandas as pd
from pymysql import Connect
con = Connect(host='localhost', port=3306, user='root', password='123456', database='edu_design')


def get_hot_city():
    sql = """select city,many_people,city_image from hot_city order by many_people desc limit 30"""
    df = pd.read_sql(sql, con)
    city_dict = dict(zip(df['city'].tolist(),df['city'].tolist()))
    df['many_key'] = df['city']+'_m'
    many_dict = dict(zip(df['many_key'].tolist(),df['many_people'].tolist()))
    df['img_key'] = df['city']+'_img'
    img_dict = dict(zip(df['img_key'].tolist(),df['city_image'].tolist()))
    city_dict.update(many_dict)
    city_dict.update(img_dict)
    return city_dict




