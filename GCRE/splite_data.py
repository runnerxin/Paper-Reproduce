import random


def run(checkin_file, least_user_num=30, random_rate=1.0):
    user_location = {}  # user 对应着location list
    location_list = []  # 单个user记录location

    ################################################################################
    # 读取check in里的数据

    fr = open(checkin_file)
    now_user = -1
    for line in fr.readlines():
        cur_line = line.strip().split('\t')

        piece_data = dict()
        piece_data['user_id'] = int(cur_line[0])
        piece_data['latitude'] = float(cur_line[2]) + 90
        piece_data['longitude'] = float(cur_line[3]) + 180
        piece_data['location_id'] = int(cur_line[4])

        # check data right
        if piece_data['latitude'] > 180 or piece_data['latitude'] < 0:
            continue
        if piece_data['longitude'] > 360 or piece_data['longitude'] < 0:
            continue
        # ------------------------

        if now_user != piece_data['user_id']:
            # add_random = random.random()
            # if (len(location_list) >= least_user_num) and (add_random < random_rate):   # 过滤掉记录少于least_user_num条的用户
            #     user_location[now_user] = location_list
            if (len(location_list) >= least_user_num) and (len(user_location) < 20):  # 最后一个用户
                user_location[now_user] = location_list
            location_list = [piece_data]
            now_user = piece_data['user_id']

        else:
            location_list.append(piece_data)

    # add_random = random.random()
    # if (len(location_list) >= least_user_num) and (add_random < random_rate):  # 最后一个用户
    #     user_location[now_user] = location_list
    if (len(location_list) >= least_user_num) and (len(user_location) < 20):  # 最后一个用户
        user_location[now_user] = location_list

    return user_location


if __name__ == '__main__':
    user_loc = run('data/Gowalla_totalCheckins.txt', random_rate=0.0003)

    f = open('data/Gowalla_1.txt', 'w')
    f.write(str(user_loc))
    f.close()

    # debug
    print(len(user_loc))
    # debug


# 42242  1.0
#
# 12644 0.3
