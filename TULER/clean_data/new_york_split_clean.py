# =============================================
# @Author   : runnerxin
# @File     : new_york_split_clean.py
# @Software : PyCharm
# @Time     : 2018/11/18 16:52
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.model_selection import train_test_split


def in_city(wei, jing):
    if (wei > 40.3) and (wei < 41.2) and (jing > -74.8) and (jing < -72.5):
        return True
    return False


def split():
    user_have_check_in = set()
    user_in_relation = set()

    # ----------------------------------------------
    fr = open('../data/Gowalla_totalCheckins.txt')
    last_user = -1
    user_go_city = False
    temp_location = []
    user_location = {}

    count = 0

    for line in fr.readlines():
        cur_line = line.strip().split('\t')

        piece_data = dict()
        piece_data['user_id'] = int(cur_line[0])
        piece_data['time'] = cur_line[1]
        piece_data['latitude'] = float(cur_line[2])
        piece_data['longitude'] = float(cur_line[3])
        piece_data['location_id'] = int(cur_line[4])

        if piece_data['user_id'] != last_user:
            if (len(temp_location) > 15) and (user_go_city is True) and (count / len(temp_location) > 0.1):
                user_location[last_user] = temp_location
                user_have_check_in.add(last_user)
                user_go_city = False

            temp_location = [piece_data]
            count = 0
            if in_city(piece_data['latitude'], piece_data['longitude']):
                user_go_city = True
                count += 1
            last_user = piece_data['user_id']
        else:
            if in_city(piece_data['latitude'], piece_data['longitude']):
                user_go_city = True
                count += 1
            temp_location.append(piece_data)

    if (len(temp_location) > 15) and (user_go_city is True) and (count / len(temp_location) > 0.1):
        user_location[last_user] = temp_location
        user_have_check_in.add(last_user)

    # print(len(user_location))
    # print(len(user_have_check_in))
    # ----------------------------------------------

    fr = open('../data/Gowalla_edges.txt')
    relation = []
    user_relation = {}

    link_count = 0
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        id1 = int(cur_line[0])
        id2 = int(cur_line[1])

        if (id1 in user_have_check_in) and (id2 in user_have_check_in):
            link_count += 1
            relation.append((id1, id2))
            user_in_relation.add(id1)
            user_in_relation.add(id2)

            if id1 not in user_relation:
                user_relation[id1] = []
            user_relation[id1].append(id2)

    # print(len(relation))
    # print(len(user_in_relation))
    # print('link:', link_count)

    user_common = user_have_check_in.intersection(user_in_relation)
    # print(len(common))
    out = user_have_check_in - user_common

    for u in out:
        del user_location[u]

    print(len(user_location))
    print(len(user_in_relation))
    print(len(user_common))
    print(link_count)
    # 1763
    # 1763
    # 1763
    # 7926

    fr = open('../middata/new_york_user_location.txt', 'w')
    fr.write(str(user_location))

    fr = open('../middata/new_york_user_relation_pair.txt', 'w')
    fr.write(str(relation))

    fr = open('../middata/new_york_user_common.txt', 'w')
    fr.write(str(list(user_common)))

    fr = open('../middata/new_york_user_relation_dict.txt', 'w')
    fr.write(str(user_relation))



# 1763
# 3963
def data():
    f = open('../middata/new_york_user_location', 'r')
    a = f.read()
    user_location = eval(a)
    f.close()

    f = open('../middata/new_york_user_relation', 'r')
    a = f.read()
    user_relation = eval(a)
    f.close()

    f = open('../middata/new_york_user_common', 'r')
    a = f.read()
    user_common = eval(a)
    f.close()

    # -----------------------------------------------------------------

    all_location = 0
    all_link = 0
    for u in user_common:
        all_location += len(user_location[u])
    for u in user_relation:
        all_link += len(user_relation[u])

    print('all------------------')
    print('user', len(user_common))
    print('location', all_location)
    print('relation', all_link)

    # -------------------------------------------------
    # # print(len(user_location))
    train_user_location = {}
    train_user_relation = {}
    # train_user = []

    test_user_location = {}
    test_user_relation = {}
    # # test_user = []

    train_user, test_user = train_test_split(list(user_common), test_size=0.5)
    # print(len(train_user), len(test_user))

    # count = 0
    train_count_location = 0
    test_count_location = 0

    for u in user_location:
        if u in train_user:
            train_user_location[u] = user_location[u]
            train_user.append(u)
            train_count_location += len(user_location[u])
        else:
            test_user_location[u] = user_location[u]
            test_user.append(u)
            test_count_location += len(user_location[u])
        # count += 1

    train_link = 0
    test_link = 0
    for u in user_relation:
        if u in train_user:
            train_user_relation[u] = [uu for uu in user_relation[u] if uu in train_user]
            train_link += len(train_user_relation[u])
        else:
            test_user_relation[u] = [uu for uu in user_relation[u] if uu in test_user]
            test_link += len(test_user_relation[u])

    print('train-------------------------')
    print('user', len(train_user_location))
    print('location', train_count_location)

    # print('relation', len(train_user_relation))
    print('relation', train_link)

    print('test---------------------------')
    print('user', len(test_user_location))
    print('location', test_count_location)

    # print('relation', len(test_user_relation))
    print('relation', test_link)

    # 1763
    # 3963

    pass


if __name__ == '__main__':
    split()


    pass