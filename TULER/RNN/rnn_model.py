# =============================================
# @Author   : runnerxin
# @File     : rnn_model.py
# @Software : PyCharm
# @Time     : 2018/11/22 14:43
# =============================================

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from RNN.model import RNN
from RNN.data_read import Data
import torch
from torch import nn
import numpy as np


def run():
    data = Data()
    model = RNN()
    # print(model)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_func = nn.MSELoss()

    for epoch in range(200):
        for sentence in data.sentences:
            x = np.array(sentence[:-1], dtype=np.float32)
            y = np.array(sentence[1:], dtype=np.float32)
            x = torch.from_numpy(x[:, np.newaxis, np.newaxis])      # shape (time_step, batch, input_size)
            y = torch.from_numpy(y[:, np.newaxis, np.newaxis])

            prediction, state = model(x)              # rnn output
            # print(prediction.shape)

            # print(prediction.shape)
            # print(h_n.shape)
            # print(h_c.shape)

            loss = loss_func(prediction, y)             # calculate loss
            print(loss)
            optimizer.zero_grad()                       # clear gradients for this training step
            loss.backward()                             # back propagation, compute gradients
            optimizer.step()                            # apply gradients

    torch.save(model, 'model.pkl')

    # y = np.array([4, 5, 6], dtype=np.float32)
    # y = torch.from_numpy(y[:, np.newaxis, np.newaxis])  # shape (time_step, batch, input_size)
    # loss = loss_func(prediction, y)
    # print(loss)
    # print(prediction)


def test():
    model = torch.load('model.pkl')
    x = np.array([3, 4, 5], dtype=np.float32)
    x = torch.from_numpy(x[:, np.newaxis, np.newaxis])  # shape (time_step, batch, input_size)
    prediction, state = model(x)
    print(prediction)
    for i in range(3):
        in_x = prediction[-1, :, :]
        in_x = in_x.view(-1, in_x.size(0), in_x.size(1))
        # state = (state[0].data, state[1].data)
        prediction, state = model(in_x, state)

        print(prediction)


if __name__ == "__main__":

    # run()
    test()


