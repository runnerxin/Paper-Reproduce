# =============================================
# @Author   : runnerxin
# @File     : data_count.py
# @Software : PyCharm
# @Time     : 2018/11/17 18:41
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-


def count():

    map_id = {}
    index = 0
    user_set = set()

    fs = open('../data/fs_data.txt')
    user_location_a = {}
    for line in fs.readlines():
        cur_line = line.strip().split('_')
        user_id = int(cur_line[0])
        x = int(float(cur_line[2]) * 10)
        y = int(float(cur_line[3]) * 10)

        user_set.add(user_id)
        if (x, y) not in map_id:
            map_id[x, y] = index
            index += 1
        if user_id not in user_location_a:
            user_location_a[user_id] = []

        user_location_a[user_id].append(map_id[x, y])

    # print(user_location_a)
    # -----------------------------------------------
    fs = open('../data/tt_data.txt')
    user_location_b = {}
    for line in fs.readlines():
        cur_line = line.strip().split('_')
        user_id = int(cur_line[0])
        x = int(float(cur_line[2]) * 10)
        y = int(float(cur_line[3]) * 10)

        user_set.add(user_id)
        if (x, y) not in map_id:
            map_id[x, y] = index
            index += 1
        if user_id not in user_location_b:
            user_location_b[user_id] = []

        user_location_b[user_id].append(map_id[x, y])

    common = set([u for u in user_location_b if u in user_location_a])
    print(len(common))

    for u in user_location_a:
        if u not in common:
            del user_location_a[u]
    for u in user_location_b:
        if u not in common:
            del user_location_b[u]
    print(len(user_location_a))
    print(len(user_location_b))


if __name__ == '__main__':
    count()


    pass
