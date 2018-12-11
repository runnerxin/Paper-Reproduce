# =============================================
# @Author   : runnerxin
# @File     : new_york_model.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:07
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-


from torch import nn


class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.location_number = 78242
        self.input_size = 200
        self.hidden_size = 64
        self.output_size = 78242
        self.num_layers = 1

        self.embedding = nn.Embedding(self.location_number, self.input_size)
        self.rnn = nn.LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=False
        )
        self.out = nn.Linear(self.hidden_size, self.output_size)
        # self.out = log_softmax

    def forward(self, x, state=None):
        # # x shape (time_step, batch, input_size)
        # # r_out shape (time_step, batch, output_size)
        # # h_n shape (n_layers, batch, hidden_size)
        # # h_c shape (n_layers, batch, hidden_size)

        x = self.embedding(x)
        r_out, state = self.rnn(x)
        r_out = r_out.view(-1, self.hidden_size)
        outs = self.out(r_out)              # 经过全连接成
        outs = outs.view(-1, x.size(1), self.output_size)
        # outs = outs.view(-1, self.output_size)

        return outs, state
