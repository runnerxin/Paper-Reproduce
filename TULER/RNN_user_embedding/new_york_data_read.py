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
        self.user = None
        self.relation = None

        self.location_2_id_dict = None
        self.id_2_location_dict = None
        self.location_number = None

        self.user_2_new_id = None
        self.new_id_2_user = None
        self.user_number = None

        self.get_data()

    def get_data(self):
        f = open('../middata/new_york_user_location.txt', 'r')
        a = f.read()
        user_location = eval(a)
        f.close()

        f = open('../middata/new_york_user_relation_pair.txt', 'r')
        a = f.read()
        relation = eval(a)
        f.close()

        # ------------------------------------------------------------
        # 给地点重新映射编号
        location_2_id_dict = {}                # 地点id 重新映射编号
        id_2_location_dict = {}                # 地点编号映射地点
        number_location = 0

        user_2_new_id = dict()
        new_id_2_user = dict()
        number_user = 0
        for user in user_location:
            if user not in user_2_new_id:
                user_2_new_id[user] = number_user
                new_id_2_user[number_user] = user
                number_user += 1

            for piece in user_location[user]:
                if piece['location_id'] not in location_2_id_dict:

                    location_2_id_dict[piece['location_id']] = number_location
                    id_2_location_dict[number_location] = {'location_id': piece['location_id'],
                                                           'latitude': piece['latitude'],
                                                           'longitude': piece['longitude']}
                    number_location += 1

        self.location_2_id_dict = location_2_id_dict
        self.id_2_location_dict = id_2_location_dict
        self.location_number = len(location_2_id_dict)

        self.user_2_new_id = user_2_new_id
        self.new_id_2_user = new_id_2_user
        self.user_number = len(user_2_new_id)

        # ------------------------------------------------------------
        # user/地点序列重新映射
        self.data = dict()
        self.user = dict()
        for user in user_location:

            # 构造序列数据
            d = []
            u = []
            for piece in user_location[user]:
                d.append(location_2_id_dict[piece['location_id']])
                u.append(user_2_new_id[user])
            d = np.array(d, dtype=np.longlong)
            u = np.array(u, dtype=np.longlong)

            # 构造结果
            self.data[user_2_new_id[user]] = torch.from_numpy(d[:, np.newaxis])
            self.user[user_2_new_id[user]] = torch.from_numpy(u[:, np.newaxis])
            # self.data[new_id] = torch.from_numpy(d[:])

        # ------------------------------------------------------------
        # user关系重新映射
        self.relation = []
        for pair in relation:
            self.relation.append((self.user_2_new_id[pair[0]], self.user_2_new_id[pair[1]]))

        pass


data = Data()


# for i in range(0,5):
#     print(data.data[i])
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
