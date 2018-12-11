# =============================================
# @Author   : runnerxin
# @File     : new_york_model.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:07
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-

import torch
from torch import nn
from RNN_user_embedding.new_york_data_read import data


class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.location_number = data.location_number
        self.user_number = data.user_number
        self.user_input_size = 100
        self.location_input_size = 100

        self.hidden_size = 64
        self.output_size = data.location_number
        self.num_layers = 1

        self.embedding_user = nn.Embedding(self.user_number, self.user_input_size)
        self.embedding_location = nn.Embedding(self.location_number, self.location_input_size)
        self.rnn = nn.LSTM(
            input_size=(self.user_input_size + self.location_input_size),
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=False
        )
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, u, x, state=None):
        # # x shape (time_step, batch, input_size)
        # # r_out shape (time_step, batch, output_size)
        # # h_n shape (n_layers, batch, hidden_size)
        # # h_c shape (n_layers, batch, hidden_size)

        u = self.embedding_user(u)
        x = self.embedding_location(x)

        new_in = torch.cat(tensors=(u, x), dim=2)
        # new_in = torch.cat((u, x), 2)

        r_out, state = self.rnn(new_in)
        # print('out', r_out.shape)

        r_out = r_out.view(-1, self.hidden_size)
        outs = self.out(r_out)              # 经过全连接成
        outs = outs.view(-1, x.size(1), self.output_size)
        # outs = outs.view(-1, self.output_size)
        # print(outs.shape)

        return outs, state
