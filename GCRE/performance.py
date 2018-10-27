
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


if __name__ == '__main__':

    # ans_file = 'data/similarity_kde.txt'
    ans_file = 'data/similarity_kde_g.txt'

    run(ans_file, 0.00003)

