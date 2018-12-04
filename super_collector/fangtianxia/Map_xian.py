# -*- coding: utf-8 -*-#

# Name:         Map_xian.py
# Author:       jiaocheng
# Date:         2018/11/22
# Description:


from pyecharts import Map, Geo, Style
import pandas as pd

# 导入excel表举例
df = pd.read_excel('D:\hadoop_test\\1.xlsx')
df.head()


# 导入自定义的地点经纬度
geo_cities_coords = {df.iloc[i]['地点']: [df.iloc[i]['经度'], df.iloc[i]['纬度']] for i in range(len(df))}
attr = list(df['地点'])
value = list(df['数量'])
style = Style(title_color="#fff", title_pos="center",
              width=1200, height=800, background_color="#404a59")



# 可视化
geo = Geo('西安租房', **style.init_style)
geo.add("", attr, value, visual_range=[0, 100], symbol_size=10,
        visual_text_color="#fff", is_piecewise=True,
        is_visualmap=True, maptype='西安', visual_split_number=10,
        geo_cities_coords=geo_cities_coords,is_legend_show=True,label_emphasis_textsize=15,label_emphasis_pos='right')

geo.render('./西安租房分布.html')





# 省和直辖市
# province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9, '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1, '其他': 1}
# provice=list(province_distribution.keys())
# values=list(province_distribution.values())
#
# # 城市 -- 指定省的城市 xx市
# city = ['郑州市', '安阳市', '洛阳市', '濮阳市', '南阳市', '开封市', '商丘市', '信阳市', '新乡市']
# values2 = [1.07, 3.85, 6.38, 8.21, 2.53, 4.37, 9.38, 4.29, 6.1]
#
# # 区县 -- 具体城市内的区县  xx县
# quxian = ['夏邑县', '民权县', '梁园区', '睢阳区', '柘城县', '宁陵县']
# values3 = [3, 5, 7, 8, 2, 4]

# maptype='china' 只显示全国直辖市和省级
# 数据只能是省名和直辖市的名称
# map = Map("中国地图",'中国地图', width=1200, height=600)
# map.add("2121", provice, values, visual_range=[0, 50],  maptype='china', is_visualmap=True,visual_text_color='#000')
# #map.show_config()
# map.render(path="./04-01中国地图.html")


# map2 = Map("陕西地图",'陕西', width=1200, height=600)
# map2.add('陕西', city, values2, visual_range=[1, 10], maptype='陕西', is_visualmap=True, visual_text_color='#000')
# map2.show_config()
# map2.render(path="./04-02陕西地图.html")

# map3 = Map("西安地图",'西安', width=1200, height=600)
# map3.add("西安", quxian, values3, visual_range=[1, 10], maptype='西安', is_visualmap=True,
#     visual_text_color='#000')
# map3.render(path="./04-03西安地图.html")




