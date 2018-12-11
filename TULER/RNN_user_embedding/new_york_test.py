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
import numpy as np
from RNN_user_embedding.new_york_data_read import data


def vector_similarity(vector1, vector2):
    return np.sum(vector1 * vector2) / (np.sqrt(np.sum(vector1**2)) * np.sqrt(np.sum(vector2**2)))


def get_user_location():

    model = torch.load('new_york_model.pkl')

    # ----------------------------------------------------------------------
    user_related_location = {}

    for user in data.data:
        print(user)

        user_vector = model.embedding_user(torch.from_numpy(np.array([user], dtype=np.longlong)))
        user_related_location[user] = user_vector.detach().numpy().reshape(-1)
        # print(user_related_location[user].shape)

    # ----------------------------------------------------------------------
    real_pair = len(data.relation)
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
            if (u1, rank[i][0]) in data.relation:
                return_true_pair += 1

    print(real_pair)
    print(return_pair)
    print(return_true_pair)


def run():
    pass


if __name__ == '__main__':
    get_user_location()
    pass
