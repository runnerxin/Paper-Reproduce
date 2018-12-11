# =============================================
# @Author   : runnerxin
# @File     : new_york_rnn.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:07
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from RNN_grid.get_data import data
from RNN_grid.new_york_model import RNN
import torch
from torch import nn


def train():
    epoch_times = 1
    lr = 0.001

    # -----------------------------------------------------
    model = RNN(data.location_number)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    loss_func = nn.CrossEntropyLoss()

    for epoch in range(epoch_times):
        all_loss = 0
        for user in data.data:
            x = data.data[user][:-1, :]
            y = data.data[user][1:, :]
            y = y.view(-1)

            prediction, state = model(x)
            prediction = prediction.view(-1, model.output_size)  # reshape x to (batch*time_step, output_size)
            y = y.view(-1)

            loss = loss_func(prediction, y)         # calculate loss
            all_loss += loss.data

            optimizer.zero_grad()                   # clear gradients for this training step
            loss.backward()                         # back propagation, compute gradients
            optimizer.step()

        print('epoch: ', epoch, '    all_loss: ',  all_loss)
        torch.save(model, './new_york_model.pkl')  # 保存模型

    # --------------------------------------------


if __name__ == '__main__':
    train()

    pass
