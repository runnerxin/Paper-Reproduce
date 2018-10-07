import os
from STL import *
import os
import time

class KDE:
    def __init__(self, _path_in_a, _path_in_b, _path_out, _user_number, _grid_granularity, _grid_range, _q_value, _h_value, _k_value, _similarity_threshold):
        self.path_in_a = _path_in_a
        self.path_in_b = _path_in_b
        self.path_out = _path_out
        self.user_number = _user_number
        self.grid_granularity = _grid_granularity
        self.grid_range = _grid_range                                   # in the form of (lat_min, lng_min, lat_max, lng_max)
        self.q_value = _q_value
        self.h_value = _h_value
        self.k_value = _k_value
        self.similarity_threshold = _similarity_threshold

    def inputdata(self, path_in):
        list = []
        list_filename = os.listdir(path_in)
        for filename in list_filename:
            temp_list = []
            infile_platform = open(path_in + "\\" + filename, "r")
            for line in infile_platform:
                list_line = line.strip("\n").split(",")
                location = map(math.fabs, [float(list_line[1]), float(list_line[2]), float(list_line[-1])])
                if self.grid_range[0] <= location[0] <= self.grid_range[2] and self.grid_range[1] <= location[1] <= self.grid_range[3]:
                    temp_list.append(location)
            if len(temp_list) > 0:
                list.append(temp_list)
        return list

    def gkrkde(self):
        list_a = self.inputdata(self.path_in_a)    # each element is a list that contains a set of locations of a user
        list_b = self.inputdata(self.path_in_b)
        grid_length_lng = (self.grid_range[3] - self.grid_range[1])/self.grid_granularity
        grid_width_lat = (self.grid_range[2] - self.grid_range[0])/self.grid_granularity
        list_grid_a, list_grid_b = [], []
        for index in range(self.grid_granularity*self.grid_granularity):
            list_grid_a.append([])
            list_grid_b.append([])

        ###################################################################################################################
        # for each grid cell, input the user id into current grid cell, i.e., list_grid
        for x in range(len(list_a)):
            for y in range(len(list_a[x])):
                lat, lng, weight = list_a[x][y]
                grid_lat_id, grid_lng_id = int((lat - self.grid_range[0])/grid_width_lat), int((lng-self.grid_range[1])/grid_length_lng)
                grid_id = grid_lng_id*self.grid_granularity + grid_lat_id
                list_grid_a[grid_id].append(x)                  # input the user id
        for x in range(len(list_b)):
            for y in range(len(list_b[x])):
                lat, lng, weight = list_b[x][y]
                grid_lat_id, grid_lng_id = int((lat - self.grid_range[0])/grid_width_lat), int((lng-self.grid_range[1])/grid_length_lng)
                grid_id = grid_lng_id*self.grid_granularity + grid_lat_id
                list_grid_b[grid_id].append(x)                  # input the user id
        ###################################################################################################################
        # compute the entropy of each grid cell, count the grid cells for each user
        list_entropy_a, list_entropy_b = [], []
        list_a_grid, list_b_grid = [], []                       # store the entropy grid of a user
        for index in range(self.user_number):
            list_entropy_a.append([])
            list_entropy_b.append([])
            list_a_grid.append([])
            list_b_grid.append([])
        ######################################################################################################################
        sum_grid_cell_weight_a = 0
        for x in range(self.grid_granularity):
            for y in range(self.grid_granularity):
                if len(list_grid_a[x*self.grid_granularity + y]) > 0:
                    H_value = 0
                    for user_id in set(list_grid_a[x*self.grid_granularity + y]):
                        user_probability = float(list_grid_a[x*self.grid_granularity + y].count(user_id))/len(list_a[user_id])
                        H_value += pow(user_probability, self.q_value)
                    D_value = math.exp(math.log(H_value)/(self.q_value - 1))             # the entropy of each grid cell
                    sum_grid_cell_weight_a += D_value
                    for user_id in set(list_grid_a[x*self.grid_granularity + y]):
                        user_probability = float(list_grid_a[x*self.grid_granularity + y].count(user_id))/len(list_a[user_id])
                        list_entropy_a[user_id].append(GridEntroy(x*self.grid_granularity + y, D_value, user_probability))
                        list_a_grid[user_id].append(x*self.grid_granularity + y)
        for index in range(self.user_number):
            for grid_cell_weight in list_entropy_a[index]:
                relative_entropy = grid_cell_weight.getentropy() / sum_grid_cell_weight_a
                grid_cell_weight.updateentropy(relative_entropy)
        ######################################################################################################################
        sum_grid_cell_weight_b = 0
        for x in range(self.grid_granularity):
            for y in range(self.grid_granularity):
                if len(list_grid_b[x*self.grid_granularity + y]) > 0:
                    H_value = 0
                    for user_id in set(list_grid_b[x*self.grid_granularity + y]):
                        user_probability = float(list_grid_b[x*self.grid_granularity + y].count(user_id))/len(list_b[user_id])
                        H_value += pow(user_probability, self.q_value)
                    D_value = math.exp(math.log(H_value)/(self.q_value - 1))             # the entropy of each grid cell
                    sum_grid_cell_weight_b += D_value
                    for user_id in set(list_grid_b[x*self.grid_granularity + y]):
                        user_probability = float(list_grid_b[x*self.grid_granularity + y].count(user_id))/len(list_b[user_id])
                        list_entropy_b[user_id].append(GridEntroy(x*self.grid_granularity + y, D_value, user_probability))
                        list_b_grid[user_id].append(x*self.grid_granularity + y)
        for index in range(self.user_number):
            for grid_cell_weight in list_entropy_b[index]:
                relative_entropy = grid_cell_weight.getentropy() / sum_grid_cell_weight_b
                grid_cell_weight.updateentropy(relative_entropy)
        #######################################################################################################################
        # calculate user similarity based on corresponding grid cells
        max_similarity = -1.
        matrix_result = []
        for x in range(self.user_number):
            temp_list = []
            for y in range(self.user_number):
                temp_list.append(0.)
            matrix_result.append(temp_list)
        for x in range(self.user_number):
            for y in range(self.user_number):
                if len(set(list_a_grid[x]).intersection(set(list_b_grid[y]))) > 0:
                    # matrix_result[x][y] += knngridentropy(list_entropy_a[x], list_entropy_b[y], self.h_value,self.grid_range, self.grid_granularity,
                    #                                       list_a_grid[x],list_b_grid[y]) / len(list_entropy_b[y])
                    # matrix_result[x][y] += knngridentropy(list_entropy_b[y], list_entropy_a[x], self.h_value,self.grid_range, self.grid_granularity,
                    #                                       list_b_grid[y],list_a_grid[x]) / len(list_entropy_a[x])
                    matrix_result[x][y] += squareregion(list_entropy_a[x], list_entropy_b[y], self.h_value,
                                                          self.grid_range, self.grid_granularity, list_a_grid[x],
                                                          list_b_grid[y], self.k_value) / len(list_entropy_b[y])
                    matrix_result[x][y] += squareregion(list_entropy_b[y], list_entropy_a[x], self.h_value,
                                                          self.grid_range, self.grid_granularity, list_b_grid[y],
                                                          list_a_grid[x], self.k_value) / len(list_entropy_a[x])
                    matrix_result[x][y] /= 2
                if matrix_result[x][y] > max_similarity:
                    max_similarity = matrix_result[x][y]

        outfile = open(self.path_out + "\\matrix.txt", "w")
        for x in range(len(list_a)):
            for y in range(len(list_b)):
                outfile.write(str(matrix_result[x][y]/max_similarity)+"\t")
            outfile.write("\n")
        outfile.close()

    def performance(self):
        list = []
        matrix_result = []
        for x in range(self.user_number):
            temp_list = []
            for y in range(self.user_number):
                temp_list.append([])
            matrix_result.append(temp_list)
        #####################################################################
        infile_matrix = open(self.path_out + "\\matrix.txt").readlines()
        for x in range(len(infile_matrix)):
            list_line = map(float, infile_matrix[x].strip("\n").split("\t")[0:-1])
            for y in range(len(list_line)):
                matrix_result[x][y] = float(list_line[y])
                if matrix_result[x][y] > 0:
                    list.append(matrix_result[x][y])
        ################################################################################
        count_ture, count_return = 0, 0
        for x in range(self.user_number):
            for y in range(self.user_number):
                if matrix_result[x][y] >= self.similarity_threshold:
                    count_return += 1
                    if x == y:
                        count_ture += 1
        precision = float(count_ture)/count_return
        recall = float(count_ture)/self.user_number
        F1 = 2*precision*recall/(precision + recall)
        return precision, recall, F1


if __name__ == "__main__":
    list_q_value = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
    list_h_value = [100, 200, 300, 400, 500, 600]
    list_k_value = [1, 3, 5, 7, 9]
    list_grid_granularity = [3000, 5000, 7000, 9000, 11000, 13000]
    list_similarity_threshold = [0.0006, 0.0008, 0.001, 0.0012, 0.0014, 0.0016]
    grid_range = [0., 0., 75., 180.]
    ######################################################################################################################
    # for k_value in list_k_value:
    #     time_start = time.clock()
    #     user_number, grid_granularity, q_value, h_value, k_value, similarity_threshold = 862, 9000, 0.1, 300, k_value, 0.001
    #     print "FS-TW parameter value::::::::::", k_value
    #     path_in_a = "E:\WeiChen\Data\FoursquareTwitter\Foursquare"
    #     path_in_b = "E:\WeiChen\Data\FoursquareTwitter\Twitter"
    #     path_out = "E:\WeiChen\Data\FoursquareTwitter\Result\GKR-KDE"
    #     kde = KDE(path_in_a, path_in_b, path_out, user_number, grid_granularity, grid_range, q_value, h_value, k_value, similarity_threshold)
    #     kde.gkrkde()
    #     precision, recall, F1 = kde.performance()
    #     time_end = time.clock()
    #     time_cost = time_end - time_start
    #     print "precision and recall :", precision, recall
    #     print "F1:", F1
    #     print "Time cost:", time_cost
    #######################################################################################################################
    list_similarity_threshold = [0.0001, 0.0002, 0.0003, 0.0004, 0.0005, 0.0006]
    for k_value in list_k_value:
        time_start = time.clock()
        user_number, grid_granularity, q_value, h_value, k_value, similarity_threshold = 1717, 9000, 0.1, 300, k_value, 0.0003
        print "FS-TW parameter value::::::::::", k_value
        path_in_a = "E:\WeiChen\Data\InstagramTwitter\Instagram"
        path_in_b = "E:\WeiChen\Data\InstagramTwitter\Twitter"
        path_out = "E:\WeiChen\Data\InstagramTwitter\Result\GKR-KDE"
        kde = KDE(path_in_a, path_in_b, path_out, user_number, grid_granularity, grid_range, q_value, h_value, k_value, similarity_threshold)
        kde.gkrkde()
        precision, recall, F1 = kde.performance()
        time_end = time.clock()
        time_cost = time_end - time_start
        print "precision and recall :", precision, recall
        print "F1:", F1
        print "Time cost:", time_cost






