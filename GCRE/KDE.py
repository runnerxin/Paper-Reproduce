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


def kh(l1, l2, h):
    return (1 / (2 * math.pi * h)) * math.exp(-math.pow(l1 - l2, 2) / (2 * h * h))


def similarity(location_list_1, location_list_2, h):
    n, m = len(location_list_1), len(location_list_2)
    ans = 0

    for li in location_list_1:
        temp = 0
        for lj in location_list_2:
            temp += kh(Location(li['latitude'], li['longitude']), Location(lj['latitude'], lj['longitude']), h)
        ans += temp / m

    return ans/n


def kde(platform_a, platform_b, h=300):
    pair = dict()
    k = 0
    for user_1 in platform_a:
        for user_2 in platform_b:
            # 两用户有地点的交集
            s1 = set([i['location_id'] for i in platform_a[user_1]])
            s2 = set([i['location_id'] for i in platform_b[user_2]])
            if len(s1.intersection(s2)) > 0:
                pair[user_1, user_2] = similarity(platform_a[user_1], platform_b[user_2], h)
                print(user_1, user_2, pair[user_1, user_2])

    f = open('data/similarity_kde.txt', 'w')
    f.write(str(pair))
    f.close()


def run():
    f = open('data/platform_A.txt', 'r')
    a = f.read()
    platform_a = eval(a)
    f.close()

    f = open('data/platform_B.txt', 'r')
    a = f.read()
    platform_b = eval(a)
    f.close()

    kde(platform_a, platform_b)


if __name__ == '__main__':
    run()
