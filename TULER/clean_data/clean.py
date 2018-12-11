# =============================================
# @Author   : runnerxin
# @File     : clean.py
# @Software : PyCharm
# @Time     : 2018/11/16 19:30
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-


def clean():
    fr = open('../data/Gowalla_totalCheckins.txt')

    location = dict()
    index = 0

    last_user = -1
    temp_location = []
    user_location = {}
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        user_id = int(cur_line[0])
        latitude = int(float(cur_line[2])*10)
        longitude = int(float(cur_line[3])*10)

        if user_id != last_user:
            if len(temp_location) > 15:
                user_location[last_user] = temp_location

            if (latitude, longitude) not in location:
                location[latitude, longitude] = index
                index += 1
            temp_location = [location[latitude, longitude]]
            last_user = user_id
        else:
            if (latitude, longitude) not in location:
                location[latitude, longitude] = index
                index += 1
            temp_location.append(location[latitude, longitude])

    if len(temp_location) > 15:
        user_location[last_user] = temp_location

    fr = open('cleaned_data.txt', 'w')
    fr.write(str(user_location))
    print(len(user_location))

    pass


def new_rate():
    f = open('cleaned_data.txt', 'r')
    a = f.read()
    # uu = eval(a)
    user_location = eval(a)
    f.close()

    pair_count = 0
    no_common = 0
    file = '../data/Gowalla_edges.txt'
    fr = open(file)

    all_pair = 0
    for line in fr.readlines():
        cur_line = line.strip().split('\t')

        id1 = int(cur_line[0])
        id2 = int(cur_line[1])

        all_pair += 1
        if (id1 in user_location) and (id2 in user_location):  # 两个user有关系
            pair_count += 1
            list1 = set(user_location[id1])  # user1访问的地点集合
            list2 = set(user_location[id2])  # user2访问的地点集合

            if len(list1.intersection(list2)) == 0:
                no_common += 1
    print(all_pair, ' ', pair_count, ' ', no_common)

    rate = no_common / pair_count
    print(rate)


if __name__ == '__main__':
    clean()
    new_rate()

    pass

