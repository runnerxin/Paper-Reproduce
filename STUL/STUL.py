from function import *
from scipy.integrate import quad
from sklearn.mixture import GaussianMixture


def similar_region(ri, ro):
    cross_number = 0
    for r in ri:
        if r in ro:
            cross_number += 1

    union_number = len(ri) + len(ro) - cross_number
    return cross_number / union_number


def fun(x):
    return 1 / (1 + x)


def region_distribution(user_region):
    w = {}
    for user in user_region:
        fi = []
        r = []
        total = 0.0
        for u in user_region:       # 除了user之外其他user的region
            if u == user:
                continue
            for rki in user_region[u]:
                r.append(rki)

        for ri in user_region[user]:
            ans = 0.0
            for ro in r:
                ans += similar_region(ri, ro)
            # print(ans)
            # print(fun(ans))
            fi.append(fun(ans))
            total += fun(ans)
        temp = []
        for i in range(len(user_region[user])):
            temp.append(fi[i]/total)

        w[user] = temp

    # for user in w:
    #     print(w[user])
    return w


def gauss_fun(x, u, sigma):
    return np.exp(-((x - u) ** 2) / (2 * sigma)) / np.sqrt((2 * np.pi * sigma))


def similar_time(u1, d21, u2, d22):
    if d21 < d22:
        temp = u1
        u1 = u2
        u2 = temp

        temp = d21
        d21 = d22
        d22 = temp
    if d21 - d22 < 0.001:
        return 0
    d1 = np.sqrt(d21)
    d2 = np.sqrt(d22)

    u21 = u1**2
    u22 = u2**2

    x1 = (np.sqrt(2 * d21 * d22 * np.log(d1/d2) - (d21 * u22 - d22 * u21) + ((u1 * d22 - u2 * d21) ** 2) / (d21 - d22))
          - (u1 * d22 - u2 * d21) / np.sqrt(d21 - d22)) / (np.sqrt(d21 - d22))
    x2 = (np.sqrt(2 * d21 * d22 * np.log(d1/d2) - (d21 * u22 - d22 * u21) + ((u1 * d22 - u2 * d21) ** 2) / (d21 - d22))
          - (u1 * d22 - u2 * d21) / np.sqrt(d21 - d22)) / (np.sqrt(d21 - d22))

    return (quad(lambda x: gauss_fun(x, u2, d22), -np.inf, x1)[0] + quad(lambda x: gauss_fun(x, u1, d21), x1, x2)[0]
            + quad(lambda x: gauss_fun(x, u2, d22), x2, np.inf)[0])


# 2010-05-22T17:50:55Z
def get_time(time):
    ans = 0
    ans = ans * 60 + np.int(time[11:13])
    ans = ans * 60 + np.int(time[14:16])
    # ans = ans * 60 + np.int(time[17:19])
    return ans


def time_distribution(user_region):
    w = {}
    t_cluster = dict()

    for user in user_region:
        time = []
        u_t = []
        total = 0
        for u in user_region:  # 除了user之外其他user的region
            for re in user_region[u]:
                for loc in re:
                    if u == user:
                        u_t.append(get_time(loc['time']))
                    else:
                        time.append(get_time(loc['time']))
                        total += 1
        k = len(user_region[user])

        gmm = GaussianMixture(n_components=k)
        u_t = np.reshape(u_t, (-1, 1))
        gmm.fit(u_t)
        u = gmm.means_
        d = gmm.covariances_[:, 0, 0]
        bb = dict()
        bb['u'] = u
        bb['d'] = d
        t_cluster[user] = bb

        all_gmm = GaussianMixture(n_components=total)
        time = np.reshape(time, (-1, 1))
        all_gmm.fit(time)
        all_u = all_gmm.means_
        # print(all_gmm.covariances_)
        all_d = all_gmm.covariances_[:, 0, 0]

        fi = []
        for i in range(len(u)):
            ans = 0.0
            for j in range(len(all_u)):
                # print(similar_time(u[i], d[i], all_u[i], all_d[i]))
                ans += similar_time(u[i], d[i], all_u[i], all_d[i])
            fi.append(fun(ans))
            total += fun(ans)

        temp = []
        for i in range(len(fi)):
            temp.append(fi[i] / total)

        w[user] = temp
    return w, t_cluster


def relation_pair(user_region, region_w, time_cluster, time_w):
    pair = []
    num = 0
    u = []
    for user in user_region:
        u.append(user)
    for i in range(len(u)):
        for j in range(i+1, len(u)):
            user_i = user_region[u[i]]
            user_j = user_region[u[j]]
            rw_i = region_w[u[i]]
            rw_j = region_w[u[j]]
            time_i_u = time_cluster[u[i]]['u']
            time_i_d = time_cluster[u[i]]['d']
            time_j_u = time_cluster[u[j]]['u']
            time_j_d = time_cluster[u[j]]['d']
            tw_i = time_w[u[i]]
            tw_j = time_w[u[j]]

            ans_r = 0
            for ri in range(len(user_i)):
                for rj in range(len(user_j)):
                    ans_r += similar_region(user_i[ri], user_j[rj]) * rw_i[ri] * rw_j[rj]

            ans_t = 0
            for ri in range(len(time_i_u)):
                for rj in range(len(time_j_u)):
                    ans_t += similar_time(time_i_u[ri], time_i_d[ri], time_j_u[rj], time_j_d[rj]) * tw_i[ri] * tw_j[rj]

            similar_user = ans_r + ans_t + ans_r*ans_t

            if similar_user > 1e-8:
                pair.append([u[i], u[j]])
                num += 1

    return pair, num


def get_f1(k, n, m):
    recall = k/n
    precision = k/m
    f1 = 2*recall*precision/(recall+precision)
    return f1


def run():
    f = open('data/user_region.txt', 'r')
    a = f.read()
    u_region = eval(a)
    f.close()

    u_w = region_distribution(u_region)
    t_w, ti_cluster = time_distribution(u_region)

    # print(u_w)
    # print(t_w)
    # print(ti_cluster)
    p, m = relation_pair(u_region, u_w, ti_cluster, t_w)
    print(p)

    f = open('data/user_network_data.txt', 'r')
    a = f.read()
    user_loc = eval(a)
    f.close()

    n = 0
    for u in user_loc:
        n += len(user_loc[u])
    n = n/2

    k = 0
    for re in p:
        if re[1] in user_loc[re[0]]:
            k += 1

    print(get_f1(k, n, m))

    # print(p)
    # print(kk)


if __name__ == '__main__':
    run()
