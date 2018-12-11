
def run(file_in, threshold):

    f = open(file_in, 'r')
    a = f.read()
    ans = eval(a)
    f.close()

    count_true, count_return, count_link = 0, 0, 0
    user = []
    for pair in ans:
        if pair[0] not in user:
            user.append(pair[0])
            count_link += 1

        if ans[pair] > threshold:
            count_return += 1
            if pair[0] == pair[1]:
                count_true += 1

    recall = count_true / count_return
    precision = count_true / count_link
    f1 = 2 * recall * precision / (recall + precision)

    print('   recall: ', recall)
    print('precision: ', precision)
    print('       f1: ', f1)


def recall(file_in):
    f = open(file_in, 'r')
    a = f.read()
    pair = eval(a)
    f.close()

    f = open('../middata/new_york_user_relation_pair.txt', 'r')
    a = f.read()
    relation_pair = eval(a)
    f.close()

    # ---------------------------------------------------

    user_rank = {}

    for i in pair:

        if i[0] not in user_rank:
            user_rank[i[0]] = []

        user_rank[i[0]].append((i[1], pair[i]))

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


    pass


if __name__ == '__main__':

    ans_file = './similarity_kde_gks.txt'
    # ans_file = 'data/similarity_kde_gkr.txt'

    # run(ans_file, 1.7*1e-6)
    recall(ans_file)
