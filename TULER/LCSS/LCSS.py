# =============================================
# @Author   : runnerxin
# @File     : LCSS.py
# @Software : PyCharm
# @Time     : 2018/11/24 20:37
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import numpy as np


class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

    def __sub__(self, other):
        # 转成弧度制
        x1, y1, x2, y2 = map(math.radians, [other.latitude, other.longitude, self.latitude, self.longitude])

        earth_radius = 6378137.0
        temp = math.sin((x1 - x2) / 2) ** 2 + math.cos(x1) * math.cos(x2) * math.sin((y1 - y2) / 2) ** 2
        distance = 2 * math.asin(math.sqrt(temp)) * earth_radius

        return distance


def same_1(a, b):
    if a['location_id'] == b['location_id']:
        return True
    return False


def lcs(list_a, list_b):
    dp = np.zeros((len(list_a)+1, len(list_b)+1))
    for i in range(1, len(list_a)+1):
        for j in range(1, len(list_b)+1):

            if same_1(list_a[i-1], list_b[j-1]) is True:
                dp[i, j] = dp[i-1, j-1] + 1
            else:
                dp[i, j] = max(dp[i-1, j], dp[i, j-1])

    return dp[len(list_a), len(list_b)]
    # print(dp[len(list_a), len(list_b)])

# 7926
# 8815
# 1006


def run():
    f = open('../middata/new_york_user_location.txt', 'r')
    a = f.read()
    user_location = eval(a)
    f.close()

    user_rank = dict()
    for user1 in user_location:
        print(user1)
        rank = []
        for user2 in user_location:
            if user1 == user2:
                continue

            ans = lcs(user_location[user1], user_location[user2])
            # print(ans)
            rank.append((user2, ans))
        rank = sorted(rank, key=lambda cus: cus[1], reverse=True)
        user_rank[user1] = rank

    file = open("./new_york_user_lcs.txt", 'w', encoding='utf8')
    file.write(str(user_rank))
    pass


def test():
    f = open('./new_york_user_lcs.txt', 'r')
    a = f.read()
    user_lcs = eval(a)
    f.close()

    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    relation_pair = eval(a)
    f.close()

    # -----------------------------------------
    real_pair = len(relation_pair)
    return_pair = 0
    return_true_pair = 0

    for user in user_lcs:
        rank = user_lcs[user]

        for i in range(min(5, len(rank))):
            return_pair += 1
            if (user, rank[i][0]) in relation_pair:
                return_true_pair += 1

    print(real_pair)
    print(return_pair)
    print(return_true_pair)


if __name__ == '__main__':
    # run()
    test()
    pass
