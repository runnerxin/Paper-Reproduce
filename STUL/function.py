import numpy as np
import datetime


def radio(x):
    return x * np.pi / 180


def map_distance(a_latitude, a_longitude, b_latitude, b_longitude):
    x1 = radio(a_latitude)
    y1 = radio(a_longitude)
    x2 = radio(b_latitude)
    y2 = radio(b_longitude)

    earth_radius = 6378137.0
    temp = np.sin((x1 - x2) / 2) ** 2 + np.cos(x1) * np.cos(x2) * np.sin((y1 - y2) / 2) ** 2
    length = 2 * earth_radius * np.arcsin(np.sqrt(temp))
    return length


# 2010-10-12T19:44:40Z
def time_differ_second(time1, time2):

    year1 = int(time1[0:4])
    month1 = int(time1[5:7])
    days1 = int(time1[8:10])
    hours1 = int(time1[11:13])
    minute1 = int(time1[14:16])
    seconds1 = int(time1[17:19])

    year2 = int(time2[0:4])
    month2 = int(time2[5:7])
    days2 = int(time2[8:10])
    hours2 = int(time2[11:13])
    minute2 = int(time2[14:16])
    seconds2 = int(time2[17:19])

    d1 = datetime.datetime(year1, month1, days1, hours1, minute1, seconds1)
    d2 = datetime.datetime(year2, month2, days2, hours2, minute2, seconds2)
    if time1 > time2:
        return (d1 - d2).seconds
    else:
        return (d2 - d1).seconds


def la(x):
    if x <= 0:
        return 1
    else:
        return 0


def nor(x):
    max_value = np.max(x)
    min_value = np.min(x)
    if (max_value - min_value) < 1e-3:
        return x/max_value
    else:
        return (x - min_value) / (max_value - min_value)


# # debug
# if __name__ == '__main__':
#
#     # p = time_differ_second('2010-10-12T15:57:20Z', '2010-10-12T19:57:20Z')
#     # print(p)
#
#    p = map_distance(30.261599404, -97.7585805953, 30.2679095833, -97.7493124167)
#    print(p)
# 1134.6839622997857

#
#     p = str_to_time_seconds('2010-10-12T15:57:20Z')
#     print(p)
#
#     print(similar_region([1, 2, 3, 4], [2, 3, 4, 5]))
