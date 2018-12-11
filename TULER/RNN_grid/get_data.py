# =============================================
# @Author   : runnerxin
# @File     : get_data.py
# @Software : PyCharm
# @Time     : 2018/12/9 14:36
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import torch
import math
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __sub__(self, other):
        # 转成弧度制
        x1, y1, x2, y2 = map(math.radians, [other.latitude, other.longitude, self.latitude, self.longitude])

        earth_radius = 6378137.0
        temp = math.sin((x1 - x2) / 2) ** 2 + math.cos(x1) * math.cos(x2) * math.sin((y1 - y2) / 2) ** 2
        distance = 2 * earth_radius * math.asin(math.sqrt(temp))

        return distance

    def get_id(self, grid_granularity=40000):

        grid_length = 360 / grid_granularity

        id_x = int((self.latitude + 90) / grid_length)
        id_y = int((self.longitude + 180) / grid_length)
        # print(id_x,id_y)
        grid_id = id_y * grid_granularity + id_x

        return grid_id


def get_new_location(gg):
    f = open('../middata/new_york_user_location.txt', 'r')
    a = f.read()
    user_location = eval(a)
    f.close()

    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    relation = eval(a)
    f.close()

    # ---------------------------------------------------------------------
    # 重新给user映射一个id
    user_2_new_id_dict = dict()
    index1 = 0
    for user in user_location:
        if user not in user_2_new_id_dict:
            user_2_new_id_dict[user] = index1
            index1 += 1
    # ---------------------------------------------------------------------
    # relation映射新的对应编号
    new_relation = []
    for pair in relation:
        new_relation.append((user_2_new_id_dict[pair[0]], user_2_new_id_dict[pair[1]]))

    # ---------------------------------------------------------------------
    # 获得新的user_location => new_user_location
    new_user_location = dict()
    earth_id_2_location = dict()
    index2 = 0

    for user in user_location:
        new_user_id = user_2_new_id_dict[user]        # 映射user
        new_user_location[new_user_id] = []
        # print(new_user_id)

        for piece in user_location[user]:

            loc = Location(piece['latitude'], piece['longitude'])
            loc_id = loc.get_id(grid_granularity=gg)
            if loc_id not in earth_id_2_location:      # 重新给新的id编号。不保留空网格
                earth_id_2_location[loc_id] = index2
                index2 += 1

            new_user_location[new_user_id].append(str(earth_id_2_location[loc_id]))    # 映射location

    #     break
    # print(new_user_location[0])
    return new_user_location, new_relation
    pass


class Data:
    def __init__(self):
        self.data = None
        self.relation = None
        self.user_number = None
        self.location_number = None
        self.get_data()

    def get_data(self):
        new_user_location, self.relation = get_new_location(40000)

        loc = set()
        self.data = dict()
        for u in new_user_location:
            d = []
            for li in new_user_location[u]:
                loc.add(li)
                d.append(np.longlong(li))
            self.data[u] = torch.from_numpy(np.array(d)[:, np.newaxis])

        self.user_number = len(self.data)
        self.location_number = len(loc)

        pass


data = Data()
# print(data.location_number)
