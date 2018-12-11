# =============================================
# @Author   : runnerxin
# @File     : new_york_data_read.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:03
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import torch


class Data:
    def __init__(self):
        self.data = None
        self.location_2_id_dict = None
        self.id_2_location_dict = None
        self.user_number = None
        self.location_number = None
        self.get_data()

    def get_data(self):
        f = open('../middata/new_york_user_location.txt', 'r')
        a = f.read()
        user_location = eval(a)
        f.close()

        # --------------------------------------------
        # 给地点重新映射编号
        location_2_id_dict = {}                # 地点id 重新映射编号
        id_2_location_dict = {}                # 地点编号映射地点
        number = 0
        for user in user_location:
            for piece in user_location[user]:
                if piece['location_id'] not in location_2_id_dict:

                    location_2_id_dict[piece['location_id']] = number
                    id_2_location_dict[number] = {'location_id': piece['location_id'],
                                                  'latitude': piece['latitude'],
                                                  'longitude': piece['longitude']}
                    number += 1
        self.location_number = len(location_2_id_dict)
        self.location_2_id_dict = location_2_id_dict
        self.id_2_location_dict = id_2_location_dict
        # --------------------------------------------
        # 地点序列重新映射
        self.data = dict()
        for user in user_location:
            d = []
            for piece in user_location[user]:
                d.append(location_2_id_dict[piece['location_id']])
            d = np.array(d, dtype=np.longlong)
            # 构造x
            self.data[user] = torch.from_numpy(d[:, np.newaxis])
            # 构造y

        self.user_number = len(self.data)
        pass


data = Data()
# print(data.id_2_location_dict[0])

# data = Data()
# for u in data.data:
#     print(data.data[u])
#     break

# data = Data()
# print(data.user_number)
# print(data.location_number)
# 1763
# 78242
