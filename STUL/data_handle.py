from function import *


def get_stay_region_candidate_points(user_location, threshold_time=60,  threshold_distance=10000):
    # print(user_location)
    # print('********************************')
    length = len(user_location)
    if length == 0:
        return []
    # print('length', length)
    candidate_points = []
    # 第一个点

    # print(user_location)
    own = [0]
    candidate_points.append(user_location[0])

    for i in range(length):
        for j in range(i+1, length):
            ok = True
            # print('-----------')
            for k in range(i+1, j+1):

                time_differ = time_differ_second(user_location[k]['time'], user_location[j]['time'])
                map_dis = map_distance(user_location[i]['latitude'], user_location[i]['longitude'],
                                       user_location[k]['latitude'], user_location[k]['longitude'])

                # print(i, j, k, ': ',k, j, time_differ,' :  ',i,k,map_dis)
                if (k is j) and (map_dis < threshold_distance):
                    continue
                elif (map_dis < threshold_distance) and (time_differ > threshold_time):
                    continue
                else:
                    ok = False
                    break

            if ok is True:
                for k in range(i+1, j+1):
                    if k not in own:
                        own.append(k)
                        candidate_points.append(user_location[k])
            else:
                break
    # 最后一个点
    if (length - 1) not in own:
        own.append(length - 1)
        candidate_points.append(user_location[length - 1])
    return candidate_points


def load_dataset(checkin_file, network_file):
    """
        Desc:
        Args:
        Returns:
    """
    user_location = {}              # user 对应着location list
    location_list = []              # 单个user记录location
    user_list = []                  # 用户列表，存着user_id

    ################################################################################
    # 读取check in里的数据

    fr = open(checkin_file)
    now_user = -1
    k = 0
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        # print(cur_line)
        k += 1
        if k % 1000 == 0:
            print(k)
        piece_data = dict()
        piece_data['user_id'] = int(cur_line[0])
        piece_data['time'] = str(cur_line[1])
        piece_data['latitude'] = float(cur_line[2])
        piece_data['longitude'] = float(cur_line[3])
        piece_data['location_id'] = int(cur_line[4])
        # print(piece_data)

        if now_user != piece_data['user_id']:
            location_list.reverse()
            stay_region = get_stay_region_candidate_points(location_list)

            if len(stay_region) >= 1:                # 过滤掉记录少于15条的用户
                user_location[now_user] = stay_region
                user_list.append(now_user)
            location_list = [piece_data]
            now_user = piece_data['user_id']
        else:
            location_list.append(piece_data)

    location_list.reverse()
    stay_region = get_stay_region_candidate_points(location_list)
    if len(stay_region) >= 1:                        # 最后一个用户
        user_location[now_user] = stay_region
        user_list.append(now_user)

    ################################################################################
    # 读取network里的数据
    user_relationship = dict()

    fr = open(network_file)
    for line in fr.readlines():
        cur_line = line.strip().split('\t')
        # print(cur_line)
        u1, u2 = int(cur_line[0]), int(cur_line[1])
        if (u1 not in user_list) or (u2 not in user_list):
            continue
        if u1 not in user_relationship:
            user_relationship[u1] = [u2]
        else:
            user_relationship[u1].append(u2)
    ################################################################################
    # 删除check in 中，没有网络结构的数据
    for _user in user_list:
        if _user not in user_relationship:
            del(user_location[_user])

    return user_location, user_relationship


if __name__ == '__main__':
    # user_loc, user_rel = load_dataset('data/loc-gowalla_totalCheckins.txt', 'data/loc-gowalla_edges.txt')
    user_loc, user_rel = load_dataset('data/Gowalla_totalCheckins.txt', 'data/Gowalla_edges.txt')
    # print(len(temp))
    # user_loc, user_rel = load_dataset('data/test_data.txt', 'data/test_network.txt')
    # user_loc, user_rel = load_dataset('data/mini_data.txt', 'data/mini_network.txt')

    # print(u)
    # print(len(user_loc))

    f = open('data/user_region_data_all.txt', 'w')
    f.write(str(user_loc))
    f.close()

    f = open('data/user_network_data_all.txt', 'w')
    f.write(str(user_rel))
    f.close()
    # 读取
    # f = open('temp_u.txt', 'r')
    # a = f.read()
    # u = eval(a)
    # f.close()
    #
    # f = open('temp_r.txt', 'r')
    # a = f.read()
    # r = eval(a)
    # f.close()
