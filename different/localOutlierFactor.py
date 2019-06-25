from sklearn.neighbors import NearestNeighbors, LocalOutlierFactor
from joblib import dump, load


def lofTrain(data):
    # fit the model
    # fit the model for outlier detection (default)
    lofclf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
    lofclf.fit(data)
    dump(lofclf, 'LocolOutlierFactor.model')


def locolOutlierFactor(data, train):
    if train:
        lofTrain(data)
        curmodel = load('decision_tree.model')
        res = curmodel.predict(data)
    else:
        lofclf = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        res = lofclf.fit(data)
    return res
