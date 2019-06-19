from sklearn.ensemble import IsolationForest
import numpy as np
from joblib import dump, load

def isolationTrain(data):
    rng = np.random.RandomState(42)
    # fit the model
    ifclf = IsolationForest(behaviour='new', max_samples=100,
                            random_state=rng, contamination='auto')
    ifclf.fit(data)
    dump(ifclf, 'IsolationForest.model')

def isolationFroest(data):
    curmodel = load('decision_tree.model')
    res = curmodel.predict(data)
    return res