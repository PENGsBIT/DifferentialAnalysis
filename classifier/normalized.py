from sklearn.preprocessing import *
import time
import datetime
import numpy as np


def formatStr(x):
    label_encoder = LabelEncoder()
    x = label_encoder.fit_transform(x)
    x = x.astype(np.float64)


def formatTime(data):
    data=data.astype('str')
    label_encoder = LabelEncoder()
    for col in range(data.shape[1]):
        temp=data[:,col]
        data[:,col] = label_encoder.fit_transform(temp)
    data=formatStructuredData(data)
    return data
    # d = []
    # for col in range(data.shape[1]):
    #     for row in range(data.shape[0]):
    #         time=data[row,col]
    #         index=d.index(time)




def date_compare(time1, time2):
    if type(time1) == type(datetime.date(1995, 10, 11)):
        t1 = time.mktime(time1)
        t2 = time.mktime(time2)
    else:
        t1 = time1
        t2 = time2
    if t1 < t2:
        return -1
    elif t1 > t2:
        return 1
    else:
        return 0


def formatStructuredData(data):
    """

    :param data: int
    :return: formatData
    """
    X_scaled = scale(data)
    return X_scaled


def formatTarget(data):
    """
    :param data: int
    """
    good = 0
    bad = 0
    avg = np.mean(data)
    for index in range(data.shape[0]):
        val = data[index]
        if val < avg:
            data[index] = 0
            good += 1
        else:
            data[index] = 1
            bad += 1
    # print(good)
    # print(bad)
    return data
