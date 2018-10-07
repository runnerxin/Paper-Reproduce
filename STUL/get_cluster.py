from function import *


def stay_region(location, t):
    length = len(location)
    point_distance = np.zeros((length, length))     # 每两个点之间的距离
    sort_distance = []                              # 地点排序

    for i in range(length):
        for j in range(i+1, length):
            point_distance[i][j] = map_distance(location[i]['latitude'], location[i]['longitude'],
                                                location[j]['latitude'], location[j]['longitude'])
            point_distance[j][i] = point_distance[i][j]
            sort_distance.append(point_distance[i][j])

    sort_distance.sort()
    index = int(len(sort_distance) * t)
    dc = sort_distance[index]                   # 截断距离 总数的2%位置

    # print('dc: ', dc)
    # ###############################################################################

    # 局部密度
    p = np.zeros((length, 1))           # 点i周围距离小于dc的数量
    for i in range(length):
        for j in range(i+1, length):
            p[i] += la(point_distance[i][j] - dc)
            p[j] += la(point_distance[i][j] - dc)

    # 求比点的局部密度大的点到该点的最小距离
    temp = np.array(p)
    temp = temp.reshape((-1))
    p_index = np.argsort(-temp)
    neighbor = np.zeros((length,), dtype=np.int)

    delta = [0] * length                 # 最小距离
    for i in range(1, length):
        delta[p_index[i]] = point_distance[p_index[i]][p_index[0]] + 0.00001    # d_i_0
        for j in range(1, i):
            if point_distance[p_index[i]][p_index[j]] < delta[p_index[i]]:
                delta[p_index[i]] = point_distance[p_index[i]][p_index[j]]
                neighbor[p_index[i]] = p_index[j]

    delta[p_index[0]] = delta[p_index[1]]
    for i in range(2, length):
        delta[p_index[0]] = min(delta[p_index[i]], delta[p_index[0]])
    p = p.reshape((-1))
    p = nor(p)
    delta = nor(delta)

    tao = []
    for i in range(length):
        tao.append(p[i] * delta[i])

    # ################################################################################
    # 确定中心的数量。tao变化明显减小的地方
    result = np.ones(length, dtype=np.int) * -1
    temp_sort = np.argsort(-np.array(tao))

    center = [temp_sort[0]]
    result[temp_sort[0]] = 0
    last = tao[temp_sort[0]]
    k = 1

    for i in range(1, len(temp_sort)):
        if (tao[temp_sort[i]] < 1e-1) and ((last - tao[temp_sort[i]]) < 1e-3):
            break

        center.append(temp_sort[i])
        result[temp_sort[i]] = k
        last = tao[temp_sort[i]]
        k += 1

    # print('--------------------')
    print(k)
    # print(center)
    # print('--------------------')

    # ################################################################################
    # 赋予每个点聚类类标
    for i in range(length):
        if result[p_index[i]] == -1:
            result[p_index[i]] = result[neighbor[p_index[i]]]

    # 划分出每个region
    region = []
    for i in range(k):
        region.append([])

    for i in range(length):
        if result[i] != -1:
            region[result[i]].append(location[i])

    return region
    # ################################################################################
    # import matplotlib.pyplot as plt
    # colors = ['red', 'brown', 'orange', 'fuchsia', 'green', 'yellow', 'aqua', 'blue',
    #           'gray', 'lime', 'sienna', 'pink']
    # # 'black',
    # plt.figure()
    # for i in range(length):
    #     index = result[i]
    #     # print(index)
    #     if index == -1:
    #         # print(-1)
    #         plt.plot(location[i]['latitude'], location[i]['longitude'], color='black', marker='.')
    #     else:
    #         # pass
    #         plt.plot(location[i]['latitude'], location[i]['longitude'], color=colors[index], marker='.')
    # plt.xlabel('x'), plt.ylabel('y')
    # plt.show()
    #
    # return region


def get_cluster(user_location, t):
    # u_region = {}
    # import matplotlib.pyplot as plt
    # plt.figure()
    # colors = ['red', 'brown', 'orange', 'fuchsia', 'green', 'yellow', 'aqua', 'blue',
    #           'gray', 'lime', 'sienna', 'pink']
    # index = 0
    # for user in user_location:
    #     # print('num_location:', len(user_location[user]))
    #     u_region[user] = stay_region(user_location[user], t)
    #     for i in u_region[user]:
    #         for j in i:
    #             # print(j)
    #             plt.plot(j['latitude'], j['longitude'], color=colors[index], marker='.')
    #     index += 1
    #
    # plt.xlabel('x'), plt.ylabel('y')
    # plt.show()

    u_region = {}
    for user in user_location:
        u_region[user] = stay_region(user_location[user], t)
    return u_region


if __name__ == '__main__':

    f = open('data/user_region_data_all.txt', 'r')
    a = f.read()
    user_loc = eval(a)
    f.close()

    user_region = get_cluster(user_loc, 0.02)

    f = open('data/user_region_all.txt', 'w')
    f.write(str(user_region))
    f.close()
