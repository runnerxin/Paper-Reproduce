import random


def run(file_in):
    all_check_in = 0
    a_check_in = 0
    b_check_in = 0
    f = open(file_in, 'r')
    a = f.read()
    user_location = eval(a)
    f.close()

    platform_a = dict()
    platform_b = dict()
    for user in user_location:
        all_check_in += len(user_location[user])

        temp_a = []
        temp_b = []

        boundary_a = random.uniform(0.2, 0.6)
        for record in user_location[user]:
            if random.random() < boundary_a:
                temp_a.append(record)

        boundary_b = random.uniform(0.4, 0.8)
        for record in user_location[user]:
            if random.random() < boundary_b:
                temp_b.append(record)

        if len(temp_a) == 0 or len(temp_b) == 0:
            continue
        else:
            platform_a[user] = temp_a
            platform_b[user] = temp_b

            a_check_in += len(temp_a)
            b_check_in += len(temp_b)

        print('user: ', user, 'plat_a: ', len(temp_a), 'plat_b: ', len(temp_b))

    print('user: ', len(user_location), ' all: ', all_check_in)
    print('user_a: ', len(platform_a), ' all: ', a_check_in)
    print('user_b: ', len(platform_b), ' all: ', b_check_in)

    f = open('data/platform_A.txt', 'w')
    f.write(str(platform_a))
    f.close()

    f = open('data/platform_B.txt', 'w')
    f.write(str(platform_b))
    f.close()


if __name__ == '__main__':
    run('data/Gowalla_1.txt')


# user:  0 plat_a:  106 plat_b:  127
# user:  2 plat_a:  1043 plat_b:  1032
# user:  4 plat_a:  66 plat_b:  94
# user:  5 plat_a:  18 plat_b:  38
# user:  7 plat_a:  15 plat_b:  47
# user:  9 plat_a:  84 plat_b:  75
# user:  10 plat_a:  46 plat_b:  83
# user:  13 plat_a:  60 plat_b:  105
# user:  15 plat_a:  49 plat_b:  74
# user:  16 plat_a:  18 plat_b:  43
# user:  17 plat_a:  99 plat_b:  144
# user:  18 plat_a:  82 plat_b:  236
# user:  19 plat_a:  122 plat_b:  133
# user:  22 plat_a:  742 plat_b:  1235
# user:  25 plat_a:  69 plat_b:  139
# user:  27 plat_a:  40 plat_b:  96
# user:  28 plat_a:  40 plat_b:  60
# user:  29 plat_a:  30 plat_b:  65
# user:  31 plat_a:  46 plat_b:  74
# user:  32 plat_a:  163 plat_b:  225
# user:  20  all:  7112
# user_a:  20  all:  2938
# user_b:  20  all:  4125

