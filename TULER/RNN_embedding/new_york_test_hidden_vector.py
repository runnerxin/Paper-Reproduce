# =============================================
# @Author   : runnerxin
# @File     : new_york_test.py
# @Software : PyCharm
# @Time     : 2018/11/24 16:18
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import torch
import math
from RNN_embedding.new_york_data_read import data
import torch.nn.functional as F
import numpy as np


def vector_similarity(vector1, vector2):
    return np.sum(vector1 * vector2) / (np.sqrt(np.sum(vector1**2)) * np.sqrt(np.sum(vector2**2)))
#
#
# def similarity(list1, list2):
#     ans = 0
#     for i in list1:
#         for j in list2:
#             ans += vector_similarity(list1[i], list2[j])
#     return ans


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


def kh(l1, l2):
    h_value = 200
    return (1 / (2 * math.pi * h_value)) * math.exp(-math.pow(l1 - l2, 2) / (2 * h_value * h_value))


def similarity(location_list_1, location_list_2):
    n, m = len(location_list_1), len(location_list_2)
    ans = 0

    for li in location_list_1:
        temp = 0
        for lj in location_list_2:
            temp += kh(Location(li['latitude'], li['longitude']),
                       Location(lj['latitude'], lj['longitude']))
        ans += temp / m

    return ans/n


def get_user_location():

    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    relation = eval(a)
    f.close()

    model = torch.load('new_york_model.pkl')

    # ----------------------------------------------------------------------
    user_related_location = {}
    # q=0
    # print(data.id_2_location_dict[0])
    for user in data.data:
        print(user)
        u = user
        x = data.data[user]

        predict, states = model(x)          # (time_step, batch, input_size)

        # # 1
        # user_related_location[u] = states[1].view(-1).data.numpy()

        # # 2
        # user_related_location[u] = states[0].view(-1).data.numpy()

        # # 3
        # hidden = states[0]
        # out = model.out(hidden).view(1, -1)
        # out = F.log_softmax(out, dim=1)
        # user_related_location[u] = out.data.numpy()

        # 4
        hidden = states[1]
        out = model.out(hidden).view(1, -1)
        out = F.log_softmax(out, dim=1)
        user_related_location[u] = out.data.numpy()

        # break
        # print(user_related_location[u])

    # ----------------------------------------------------------------------
    real_pair = len(relation)
    return_pair = 0
    return_true_pair = 0

    for u1 in user_related_location:
        print(u1)
        rank = []
        for u2 in user_related_location:
            if u1 == u2:
                continue
            ans = vector_similarity(user_related_location[u1], user_related_location[u2])
            rank.append((u2, ans))

        # 排名
        rank = sorted(rank, key=lambda cus: cus[1], reverse=True)
        for i in range(min(5, len(rank))):
            return_pair += 1
            if (u1, rank[i][0]) in relation:
                return_true_pair += 1

    print(real_pair)
    print(return_pair)
    print(return_true_pair)


def run():
    pass


if __name__ == '__main__':
    get_user_location()
    pass
