# =============================================
# @Author   : runnerxin
# @File     : new_york_rnn.py
# @Software : PyCharm
# @Time     : 2018/11/22 20:07
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-
from RNN.new_york_data_read import Data
from RNN.new_york_model import RNN
import torch
from torch import nn


def train():
    epoch_times = 3
    lr = 0.01

    # user_vector = dict()

    # -----------------------------------------------------
    data = Data()
    model = RNN()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    # loss_func = nn.CrossEntropyLoss()
    loss_func = nn.MSELoss()

    for epoch in range(epoch_times):
        for i in range(len(data.d)):
            x = data.d[i][:-1, :, :]
            y = data.d[i][1:, :, :]
            # u = data.u[i]

            # print(x.shape)
            # print(y.shape)
            # break

            prediction, state = model(x)
            # prediction = prediction[:-1, :, :]
            # user_vec = prediction[-1, :, :]
            # user_vector[u] = user_vec.view(-1).detach().numpy().tolist()

            prediction = prediction.view(-1, model.output_size)  # reshape x to (batch*time_step, output_size)
            y = y.view(-1, model.output_size)

            loss = loss_func(prediction, y)  # calculate loss
            print(loss)

            optimizer.zero_grad()  # clear gradients for this training step
            loss.backward()  # back propagation, compute gradients
            optimizer.step()

        torch.save(model, './new_york_model.pkl')  # 保存模型

        # file = open("./new_york_user_vector.txt", 'w', encoding='utf8')
        # file.write(str(user_vector))

    # --------------------------------------------

    # pass


if __name__ == '__main__':
    train()

    # print(len(data.x))
    # print(data.x[0].shape)        # torch.Size([224, 1, 100])
    # print(data.y[0].shape)        # torch.Size([224, 1, 100])
    # print(data.d[0].shape)        # torch.Size([225, 1, 100])

    pass
