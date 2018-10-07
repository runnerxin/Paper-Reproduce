import os
import time
import math
pi = 3.1415926
R = 6371

def comlength(lat1, lng1, lat2, lng2):
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
    dlat = lat2 - lat1
    dlon = lng2 - lng1
    a = math.sin(dlon/2)**2 + math.cos(lng1) * math.cos(lng2) * math.sin(dlat/2)**2
    distance = 2*math.asin(math.sqrt(a))*6371.*1000
    return distance

def listkde(list_a, list_b, h):
    distance = 0
    length_a, length_b = len(list_a), len(list_b)
    for x in range(len(list_a)):
        temp_distance = 0
        lat_a, lng_a, location_weight = list_a[x]
        for y in range(len(list_b)):
            lat_b, lng_b, location_weight = list_b[y]
            euclidean_distance = comlength(lat_a, lng_a, lat_b, lng_b)
            temp_distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))
        temp_distance /= length_b
        distance += temp_distance

    # length_b = len(list_b)
    # for x in range(len(list_b)):
    #     temp_distance = 0
    #     lat_b, lng_b, location_weight = list_b[x]
    #     for y in range(len(list_a)):
    #         lat_a, lng_a, location_weight = list_a[y]
    #         euclidean_distance = comlength(lat_b, lng_b, lat_a, lng_a)
    #         temp_distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))
    #     temp_distance /= length_b
    #     distance += temp_distance
    return distance/length_a

def listkdeentropy(list_a, list_b, h):
    distance = 0
    length_a = len(list_a)
    for x in range(len(list_a)):
        temp_distance = 0
        lat_a, lng_a, location_weight_a = list_a[x]
        for y in range(len(list_b)):
            lat_b, lng_b, location_weight_b = list_b[y]
            euclidean_distance = comlength(lat_a, lng_a, lat_b, lng_b)
            temp_distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))*location_weight_a*location_weight_b
        temp_distance /= length_a
        distance += temp_distance

    # length_b = len(list_b)
    # for x in range(len(list_b)):
    #     temp_distance = 0
    #     lat_b, lng_b, location_weight_b = list_b[x]
    #     for y in range(len(list_a)):
    #         lat_a, lng_a, location_weight_a = list_a[y]
    #         euclidean_distance = comlength(lat_b, lng_b, lat_a, lng_a)
    #         temp_distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))*location_weight_a*location_weight_b
    #     temp_distance /= length_b
    #     distance += temp_distance
    return distance

def pointkde(location, list, h):
    distance = 0
    lat_a, lng_a = location[0], location[1]
    for x in range(len(list)):
        lat_b, lng_b = list[x]
        euclidean_distance = comlength(lat_a, lng_a, lat_b, lng_b)
        distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))
    distance /= len(list)
    return distance

def knngridentropy(list_a, list_b, h, grid_range, grid_granularity, list_a_grid, list_b_grid):
    distance = 0
    grid_length_lng = (grid_range[3] - grid_range[1])/grid_granularity
    grid_width_lat = (grid_range[2] - grid_range[0])/grid_granularity
    for element_a in list_a:
        grid_id_a, entropy_a, probability_a = element_a.getgridentropy()
        lng_a = grid_range[1] + grid_id_a/grid_granularity*grid_length_lng + 0.5*grid_length_lng
        lat_a = grid_range[0] + (grid_id_a - int(grid_id_a/grid_granularity)*grid_granularity)*grid_width_lat + 0.5*grid_width_lat
        #################################################################################################################################################
        # enumerate grid cells around the grid_a, i.e., the surrounding grid cells of the grid_a
        list_surround_grid_a = []
        if grid_id_a + grid_granularity - 1 >= 0 and list_b_grid.__contains__(grid_id_a + grid_granularity - 1):
            index = list_b_grid.index(grid_id_a + grid_granularity - 1)
            list_surround_grid_a.append(index)
        if list_b_grid.__contains__(grid_id_a + grid_granularity):
            index = list_b_grid.index(grid_id_a + grid_granularity)
            list_surround_grid_a.append(index)
        if list_b_grid.__contains__(grid_id_a + grid_granularity + 1):
            index = list_b_grid.index(grid_id_a + grid_granularity + 1)
            list_surround_grid_a.append(index)
        ######################################################################
        if grid_id_a - 1 >= 0 and list_b_grid.__contains__(grid_id_a - 1):
            index = list_b_grid.index(grid_id_a - 1)
            list_surround_grid_a.append(index)
        if list_b_grid.__contains__(grid_id_a):
            index = list_b_grid.index(grid_id_a)
            list_surround_grid_a.append(index)
        if list_b_grid.__contains__(grid_id_a + 1):
            index = list_b_grid.index(grid_id_a + 1)
            list_surround_grid_a.append(index)
        ######################################################################
        if grid_id_a - grid_granularity - 1 >= 0 and list_b_grid.__contains__(grid_id_a - grid_granularity - 1):
            index = list_b_grid.index(grid_id_a - grid_granularity - 1)
            list_surround_grid_a.append(index)
        if grid_id_a - grid_granularity >= 0 and list_b_grid.__contains__(grid_id_a - grid_granularity):
            index = list_b_grid.index(grid_id_a - grid_granularity)
            list_surround_grid_a.append(index)
        if grid_id_a - grid_granularity + 1 >= 0 and list_b_grid.__contains__(grid_id_a - grid_granularity + 1):
            index = list_b_grid.index(grid_id_a - grid_granularity + 1)
            list_surround_grid_a.append(index)
        ######################################################################
        for index in list_surround_grid_a:
            grid_id_b, entropy_b, probability_b = list_b[index].getgridentropy()
            lng_b = grid_range[1] + grid_id_b/grid_granularity*grid_length_lng + 0.5*grid_length_lng
            lat_b = grid_range[0] + (grid_id_b - int(grid_id_b/grid_granularity)*grid_granularity)*grid_width_lat + 0.5*grid_width_lat
            euclidean_distance = comlength(lat_a, lng_a, lat_b, lng_b)
            distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))*entropy_a*entropy_b*probability_a*probability_b
    return distance

def squareregion(list_a, list_b, h, grid_range, grid_granularity, list_a_grid, list_b_grid, k_value):
    distance = 0
    grid_length_lng = (grid_range[3] - grid_range[1])/grid_granularity
    grid_width_lat = (grid_range[2] - grid_range[0])/grid_granularity
    for element_a in list_a:      # a list contains a set of grid cell class, where it contains more than one record
        grid_id_a, entropy_a, probability_a = element_a.getgridentropy()
        #################################################################################################################################################
        # enumerate grid cells around the grid_a, i.e., the surrounding grid cells of the grid_a
        # the center located in coordinate (0, 0)
        list_surround_grid_a = []
        if k_value == 1:
            if list_b_grid.__contains__(grid_id_a):
                index = list_b_grid.index(grid_id_a)
                list_surround_grid_a.append(index)
        else:
            squareregion_length = k_value/2
            a_y = int(grid_id_a/grid_granularity)
            a_x = grid_id_a - a_y*grid_granularity
            for x in range(-squareregion_length, squareregion_length):
                for y in range(-squareregion_length, squareregion_length):
                    if a_x + x < 0 or a_x + x > grid_granularity or a_y + y < 0 or a_y + y > grid_granularity:
                        break
                    else:
                        b_x, b_y = a_x + x, a_y + y
                        grid_id_new = b_y*grid_granularity + b_x    # the new grid cell whether be contained by the second user
                        if list_b_grid.__contains__(grid_id_new):
                            index = list_b_grid.index(grid_id_new)
                            list_surround_grid_a.append(index)
        ###################################################################################################################################
        lng_a = grid_range[1] + grid_id_a/grid_granularity*grid_length_lng + 0.5*grid_length_lng
        lat_a = grid_range[0] + (grid_id_a - int(grid_id_a/grid_granularity)*grid_granularity)*grid_width_lat + 0.5*grid_width_lat
        for index in list_surround_grid_a:
            grid_id_b, entropy_b, probability_b = list_b[index].getgridentropy()
            lng_b = grid_range[1] + grid_id_b/grid_granularity*grid_length_lng + 0.5*grid_length_lng
            lat_b = grid_range[0] + (grid_id_b - int(grid_id_b/grid_granularity)*grid_granularity)*grid_width_lat + 0.5*grid_width_lat
            euclidean_distance = comlength(lat_a, lng_a, lat_b, lng_b)
            distance += 1./(2*math.pi)/h*math.exp(-math.pow(euclidean_distance, 2)/(2*pow(h, 2)))*entropy_a*entropy_b*probability_a*probability_b
    return distance

class GridEntroy:
    def __init__(self, _grid_id, _entropy, _probability):
        self.grid_id = _grid_id
        self.entropy = _entropy
        self.probability = _probability

    def getgridentropy(self):
        return self.grid_id, self.entropy, self.probability

    def updateentropy(self, _new_entropy):
        self.entropy = _new_entropy

    def getentropy(self):
        return self.entropy


