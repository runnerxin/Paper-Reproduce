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
        distance = 2 * earth_radius * math.asin(math.sqrt(temp))

        return distance


class Kde:
    def __init__(self, path_a, h_value):
        self.path_a = path_a
        self.h_value = h_value

    def kh(self, l1, l2):
        return (1 / (2 * math.pi * self.h_value)) * math.exp(-math.pow(l1 - l2, 2) / (2 * self.h_value * self.h_value))

    def similarity(self, location_list_1, location_list_2):
        n, m = len(location_list_1), len(location_list_2)
        ans = 0

        for li in location_list_1:
            temp = 0
            for lj in location_list_2:
                temp += self.kh(Location(li['latitude'], li['longitude']),
                                Location(lj['latitude'], lj['longitude']))
            ans += temp / m

        return ans/n

    def run(self):
        f = open(self.path_a, 'r')
        a = f.read()
        platform_a = eval(a)
        f.close()

        # f = open('data/platform_B.txt', 'r')
        # a = f.read()
        # platform_b = eval(a)
        # f.close()

        # -------------------------------------------------------------------------------------------
        user_rank = {}
        for user_1 in platform_a:
            print(user_1)
            user_rank[user_1] = []
            for user_2 in platform_a:
                if user_1 == user_2:
                    continue
                # 两用户有地点的交集
                s1 = set([i['location_id'] for i in platform_a[user_1]])
                s2 = set([i['location_id'] for i in platform_a[user_2]])
                if len(s1.intersection(s2)) > 0:
                    ans = self.similarity(platform_a[user_1], platform_a[user_2])
                    user_rank[user_1].append((user_2, ans))

        # f = open('data/similarity_kde.txt', 'w')
        # f.write(str(ans))
        # f.close()
        f = open('../middata/new_york_user_relation_pair.txt', 'r')
        a = f.read()
        relation_pair = eval(a)
        f.close()

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

        print(real_pair)
        print(return_pair)
        print(return_true_pair)


if __name__ == '__main__':
    model = Kde(path_a='../middata/new_york_user_location.txt',
                h_value=300)

    model.run()
