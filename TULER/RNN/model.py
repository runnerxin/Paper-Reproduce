# =============================================
# @Author   : runnerxin
# @File     : model.py
# @Software : PyCharm
# @Time     : 2018/11/21 15:30
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from torch import nn
import torch
import numpy as np


class RNN(nn.Module):
    def __init__(self):
        super(RNN, self).__init__()
        self.input_size = 1
        self.hidden_size = 32
        self.output_size = 1
        self.num_layers = 1

        self.rnn = nn.LSTM(
            input_size=self.input_size,
            hidden_size=self.hidden_size,
            num_layers=self.num_layers,
            batch_first=False
        )
        self.out = nn.Linear(self.hidden_size, self.output_size)

    def forward(self, x, state=None):
        # # x shape (time_step, batch, input_size)
        # # r_out shape (time_step, batch, output_size)
        # # h_n shape (n_layers, batch, hidden_size)
        # # h_c shape (n_layers, batch, hidden_size)

        # r_out, state = self.rnn(x)
        # ans = []
        # # print(self.out(r_out[-1, :, :]).shape)
        # for time_step in range(x.size(0)):
        #     # print(self.out(r_out[-1, :, :]).view(-1, 1, 1).shape)
        #     # print(state)
        #
        #     # new_x = torch.from_numpy(np.zeros((1,), dtype=np.float32)[:, np.newaxis, np.newaxis])
        #
        #     new_x = self.out(r_out[-1, :, :]).view(-1, 1, 1)
        #     r_out, state = self.rnn(new_x, state)
        #     # print(state)
        #     ans.append(self.out(r_out[-1, :, :]))
        #     # print(ans)
        # return torch.stack(ans, dim=0), state

        r_out, state = self.rnn(x, state)
        r_out = r_out.view(-1, self.hidden_size)
        outs = self.out(r_out)              # 经过全连接成
        outs = outs.view(-1, x.size(1), self.output_size)

        return outs, state
