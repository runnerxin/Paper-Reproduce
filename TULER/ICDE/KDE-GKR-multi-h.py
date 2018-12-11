# =============================================
# @Author   : runnerxin
# @File     : KDE-GKR.py
# @Software : PyCharm
# @Time     : 2018/11/17 14:17
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import multiprocessing


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


class KdeGKR:
    def __init__(self, path_a, grid_granularity, h_value, k_value, q_value):
        self.path_a = path_a
        self.grid_granularity = grid_granularity
        self.h_value = h_value
        self.k_value = k_value
        self.q_value = q_value

        self.grid_id_of_center = dict()  # 标记每个grid的中心，方便后续计算
        # 42 > latitude > 40        -71 > longitude > -74.8
        # (41.2 > latitude > 40.3) (-72.5 > longitude > -74.8)

    def kh(self, l1, l2, w1, w2, se_1, se_2):
        temp = (1 / (2 * math.pi * self.h_value))
        temp = temp * math.exp(-math.pow(l1 - l2, 2) / (2 * self.h_value * self.h_value))
        temp = temp * w1 * w2 * se_1 * se_2
        return temp

    def similarity(self, grid_list_1, grid_list_2, grid_weight_1, grid_weight_2, renyi_entropy_a, renyi_entropy_b):
        n, m = len(grid_list_1), len(grid_list_2)
        region_length = self.k_value // 2
        ans = 0

        for id_1 in grid_list_1:
            temp = 0
            now_latitude_id = id_1 // self.grid_granularity
            now_longitude_id = id_1 % self.grid_granularity

            # 获取id_1范围内k*k的格子
            for x in range(-region_length, region_length):
                for y in range(-region_length, region_length):
                    new_x, new_y = now_latitude_id + x, now_longitude_id + y
                    # 超出范围的不取
                    if (new_x < 0) or (new_x >= self.grid_granularity) \
                            or (new_y < 0) or (new_y >= self.grid_granularity):
                        continue
                    else:
                        # 构造新的id_2，并判断是否存在user2中
                        id_2 = new_x * self.grid_granularity + new_y
                        if id_2 not in grid_weight_2:
                            continue

                        gl1 = Location(self.grid_id_of_center[id_1]['latitude'],
                                       self.grid_id_of_center[id_1]['longitude'])
                        gl2 = Location(self.grid_id_of_center[id_2]['latitude'],
                                       self.grid_id_of_center[id_2]['longitude'])
                        wl1 = grid_weight_1[id_1]
                        wl2 = grid_weight_2[id_2]

                        # print(renyi_entropy_b[id_2])
                        se_1 = math.pow(renyi_entropy_a[id_1], 1.0 / (self.q_value - 1))
                        se_2 = math.pow(renyi_entropy_b[id_2], 1.0 / (self.q_value - 1))
                        # print(se_2)

                        temp += self.kh(gl1, gl2, wl1, wl2, se_1, se_2)

            ans += temp / m
        return ans/n

    def run(self, relation_pair, platform_a):

        grid_latitude_length = 180 / self.grid_granularity   # 每格多宽
        grid_longitude_length = 360 / self.grid_granularity

        # -------------------------------------------------------------------------------------------
        # 计算platform_a
        grid_contain_a = dict()
        grid_weight_a = dict()
        renyi_entropy_a = dict()

        for user in platform_a:
            # 获得grid list
            grid_contain_a[user] = []
            for check in platform_a[user]:
                latitude_id = int(check['latitude']/grid_latitude_length)
                longitude_id = int(check['longitude']/grid_longitude_length)
                grid_id = latitude_id * self.grid_granularity + longitude_id
                grid_contain_a[user].append(grid_id)

                self.grid_id_of_center[grid_id] = {'latitude': (latitude_id + 0.5) * grid_latitude_length,
                                                   'longitude': (longitude_id + 0.5) * grid_longitude_length}

            # 计算grid 权重
            weight = dict()
            for grid_id_count in set(grid_contain_a[user]):
                weight[grid_id_count] = grid_contain_a[user].count(grid_id_count) / len(grid_contain_a[user])

                if grid_id_count not in renyi_entropy_a:
                    renyi_entropy_a[grid_id_count] = math.pow(weight[grid_id_count], self.q_value)
                else:
                    renyi_entropy_a[grid_id_count] += math.pow(weight[grid_id_count], self.q_value)

            grid_weight_a[user] = weight

        # # --------------------------------
        # # 计算platform_b
        # grid_contain_b = dict()
        # grid_weight_b = dict()
        # renyi_entropy_b = dict()
        # for user in platform_b:
        #     # 获得grid list
        #     grid_contain_b[user] = []
        #     for check in platform_b[user]:
        #         latitude_id = int(check['latitude']/grid_latitude_length)
        #         longitude_id = int(check['longitude']/grid_longitude_length)
        #         grid_id = latitude_id * self.grid_granularity + longitude_id
        #         grid_contain_b[user].append(grid_id)
        #
        #         self.grid_id_of_center[grid_id] = {'latitude': (latitude_id + 0.5) * grid_latitude_length,
        #                                            'longitude': (longitude_id + 0.5) * grid_longitude_length}
        #
        #     # 计算grid 权重
        #     weight = dict()
        #     for grid_id_count in set(grid_contain_b[user]):
        #         weight[grid_id_count] = grid_contain_b[user].count(grid_id_count) / len(grid_contain_b[user])
        #
        #         if grid_id_count not in renyi_entropy_b:
        #             renyi_entropy_b[grid_id_count] = math.pow(weight[grid_id_count], self.q_value)
        #         else:
        #             renyi_entropy_b[grid_id_count] += math.pow(weight[grid_id_count], self.q_value)
        #
        #     grid_weight_b[user] = weight

        # -------------------------------------------------------------------------------------------
        # 计算user之间的相识度
        user_rank = {}
        for user_1 in grid_contain_a:
            print(user_1)
            user_rank[user_1] = []
            for user_2 in grid_contain_a:
                if user_1 == user_2:
                    continue
                # 两用户有地点的交集
                if len(set(grid_contain_a[user_1]).intersection(set(grid_contain_a[user_2]))) > 0:
                    ans = self.similarity(grid_contain_a[user_1], grid_contain_a[user_2],
                                          grid_weight_a[user_1], grid_weight_a[user_2],
                                          renyi_entropy_a, renyi_entropy_a)
                    user_rank[user_1].append((user_2, ans))

        # file = open("./new_york_user_rank.txt", 'w', encoding='utf8')
        # file.write(str(user_rank))
        # -------------------------------------------------------------------------------------------

        real_pair = len(relation_pair)
        return_pair = 0
        return_true_pair = 0
        for user in user_rank:
            rank = user_rank[user]
            rank = sorted(rank, key=lambda cus: cus[1], reverse=True)

            for i in range(min(5, len(rank))):
                return_pair += 1
                if (user, rank[i][0]) in relation_pair:
                    return_true_pair += 1

        # print(real_pair)
        # print(return_pair)
        # print(return_true_pair)
        return real_pair, return_pair, return_true_pair


def multi_run(g, h, k, q, relation_pair, platform_a):

    model = KdeGKR(path_a='../middata/new_york_user_location.txt',
                   grid_granularity=g,
                   h_value=h,
                   k_value=k,
                   q_value=q)
    a, b, c = model.run(relation_pair, platform_a)
    print(model.grid_granularity, model.h_value, model.k_value, model.q_value, '|', a, b, c)


if __name__ == '__main__':
    # run()
    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    rp = eval(a)
    f.close()

    f = open('../middata/new_york_user_location.txt', 'r')
    a = f.read()
    pa = eval(a)
    f.close()

    jobs = []
    for i in range(50, 1000, 50):
        p = multiprocessing.Process(target=multi_run, args=(57000, i, 3, 0.1, rp, pa))
        # g h k q
        jobs.append(p)
        p.start()

