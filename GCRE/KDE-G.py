import math


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


class Gkde:
    def __init__(self, path_a, path_b, grid_granularity, h_value, similarity_threshold):
        self.path_a = path_a
        self.path_b = path_b
        self.grid_granularity = grid_granularity
        self.h_value = h_value
        self.similarity_threshold = similarity_threshold

        self.grid_id_of_center = dict()  # 标记每个grid的中心，方便后续计算

    def kh(self, l1, l2, w1, w2):
        temp = (1 / (2 * math.pi * self.h_value))
        temp = temp * math.exp(-math.pow(l1 - l2, 2) / (2 * self.h_value * self.h_value))
        temp = temp * w1 * w2
        return temp

    def similarity(self, grid_list_1, grid_list_2, grid_weight_1, grid_weight_2):
        n, m = len(grid_list_1), len(grid_list_2)
        ans = 0

        for id_1 in grid_list_1:
            temp = 0
            for id_2 in grid_list_2:
                gl1 = Location(self.grid_id_of_center[id_1]['latitude'], self.grid_id_of_center[id_1]['longitude'])
                gl2 = Location(self.grid_id_of_center[id_2]['latitude'], self.grid_id_of_center[id_2]['longitude'])
                wl1 = grid_weight_1[id_1]
                wl2 = grid_weight_2[id_2]
                temp += self.kh(gl1, gl2, wl1, wl2)
            ans += temp / m

        return ans/n

    def run(self):
        f = open(self.path_a, 'r')
        a = f.read()
        platform_a = eval(a)
        f.close()

        f = open(self.path_b, 'r')
        a = f.read()
        platform_b = eval(a)
        f.close()

        grid_latitude_length = 180 / self.grid_granularity   # 每格多宽
        grid_longitude_length = 360 / self.grid_granularity

        # -------------------------------------------------------------------------------------------
        # 计算platform_a
        grid_contain_a = dict()
        grid_weight_a = dict()

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
            grid_weight_a[user] = weight

        # --------------------------------
        # 计算platform_b
        grid_contain_b = dict()
        grid_weight_b = dict()
        for user in platform_b:
            # 获得grid list
            grid_contain_b[user] = []
            for check in platform_b[user]:
                latitude_id = int(check['latitude']/grid_latitude_length)
                longitude_id = int(check['longitude']/grid_longitude_length)
                grid_id = latitude_id * self.grid_granularity + longitude_id
                grid_contain_b[user].append(grid_id)

                self.grid_id_of_center[grid_id] = {'latitude': (latitude_id + 0.5) * grid_latitude_length,
                                                   'longitude': (longitude_id + 0.5) * grid_longitude_length}

            # 计算grid 权重
            weight = dict()
            for grid_id_count in set(grid_contain_b[user]):
                weight[grid_id_count] = grid_contain_b[user].count(grid_id_count) / len(grid_contain_b[user])
            grid_weight_b[user] = weight

        # -------------------------------------------------------------------------------------------
        # 计算user之间的相识度
        pair = dict()
        for user_1 in grid_contain_a:
            for user_2 in grid_contain_b:
                # 两用户有地点的交集
                if len(set(grid_contain_a[user_1]).intersection(set(grid_contain_b[user_2]))) > 0:
                    pair[user_1, user_2] = self.similarity(grid_contain_a[user_1], grid_contain_b[user_2],
                                                           grid_weight_a[user_1], grid_weight_b[user_2])

                    print(user_1, user_2, pair[user_1, user_2])

        # -------------------------------------------------------------------------------------------
        f = open('data/similarity_kde_g.txt', 'w')
        f.write(str(pair))
        f.close()


if __name__ == '__main__':
    # run()
    model = Gkde(path_a='data/platform_A.txt',
                 path_b='data/platform_B.txt',
                 grid_granularity=3000,
                 h_value=300,
                 similarity_threshold=1e-5)

    model.run()
