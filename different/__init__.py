from different.isolation import *
from different.localOutlierFactor import *
from different.entropy import paritionEntropy


def differInterval(data, des):
    for i in range(data.shape[1]):
        col = data[:, i]
        # exc = isolationFroest(col, train=False)
        exc = []
        # lofTrain(data, train=False)
        paritionEntropy(data, exc, des)
