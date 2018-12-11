# =============================================
# @Author   : runnerxin
# @File     : new_york_test.py
# @Software : PyCharm
# @Time     : 2018/11/24 16:18
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import torch
import numpy as np
from RNN.new_york_data_read import Data


def vector_similarity(vector1, vector2):
    return np.sum(vector1 * vector2) / (np.sqrt(np.sum(vector1**2)) * np.sqrt(np.sum(vector2**2)))


def similarity(list1, list2):
    # print(list1)
    # print(list2)
    ans = 0
    for vi in list1:
        for vj in list2:
            ans += vector_similarity(vi, vj)
    return ans


def get_user_vector():
    # f = open('./new_york_user_vector.txt', 'r')
    # a = f.read()
    # user_vector = eval(a)
    # f.close()

    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    relation = eval(a)
    f.close()

    model = torch.load('new_york_model.pkl')
    data = Data()

    # ----------------------------------------------------------------------
    user_related_location = {}
    for i in range(len(data.u)):
        print(i)
        u = data.u[i]
        x = data.d[i]

        predict, states = model(x)
        user_related_location[u] = [predict[-1:, :, :].view(-1).detach().numpy()]

        for j in range(3):
            x2 = predict[-1, :, :]
            x2 = x2.view(-1, x2.size(0), x2.size(1))
            predict, states = model(x2, states)
            user_related_location[u].append(predict[-1:, :, :].view(-1).detach().numpy())

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
            ans = similarity(user_related_location[u1], user_related_location[u2])
            rank.append((u2, ans))

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
    get_user_vector()
    pass
