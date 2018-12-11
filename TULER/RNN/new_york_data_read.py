# =============================================
# @Author   : runnerxin
# @File     : new_york_data_read.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:03
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import torch
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
from gensim.models import word2vec


class Data:
    def __init__(self):
        self.u = None
        # self.x = None
        # self.y = None
        self.d = None
        self.get_data()

    def get_data(self):
        f = open('../middata/new_york_user_sentence.txt', 'r')
        a = f.read()
        user_sentence = eval(a)
        f.close()

        vec_model = word2vec.Word2Vec.load('../middata/new_york_embedding.model')

        self.u = []
        # self.x = []
        # self.y = []
        self.d = []

        for user in user_sentence:
            location_list = user_sentence[user]
            # piece_x = np.array(vec_model[location_list[:-1]], dtype=np.float32)
            # piece_y = np.array(vec_model[location_list[1:]], dtype=np.float32)
            piece_l = np.array(vec_model[location_list[:]], dtype=np.float32)

            # piece_x = torch.from_numpy(piece_x[:, np.newaxis, :])  # shape (time_step, batch, input_size)
            # piece_y = torch.from_numpy(piece_y[:, np.newaxis, :])  # shape (time_step, batch, input_size)
            piece_l = torch.from_numpy(piece_l[:, np.newaxis, :])  # shape (time_step, batch, input_size)

            # print(piece_x.shape)

            self.u.append(user)
            # self.x.append(piece_x)
            # self.y.append(piece_y)
            self.d.append(piece_l)

            # break
        pass
