from sklearn.tree import DecisionTreeClassifier, tree
from sklearn.tree.export import export_graphviz
import tensorflow as tf
from tensorflow import keras
import numpy as np
from joblib import dump, load
from sklearn.tree.export import export_text
from sklearn.metrics import accuracy_score


def classifierTraining(data, sData, time, target, colName):
    target = target.astype('int')
    temp = np.concatenate((sData, time), axis=1)
    decision_tree = DecisionTreeClassifier(random_state=1, max_depth=5)
    decision_tree = decision_tree.fit(temp, target)
    dump(decision_tree, 'decision_tree.model')
    sCol = ["view", "size", "subsets", "created", "updated"]
    r = export_text(decision_tree, feature_names=sCol)
    print(r)
    predict = decision_tree.predict(sData)
    print(accuracy_score(target, predict))


def DNNclassiferTraining(data, sData, time, target, colName):
    target = target.astype('int')
    temp = np.concatenate((sData, time), axis=1)
    # 每行数据3个特征，都是real-value的
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=3)]

    # 构建一个DNN分类器，3层，其中每个隐含层的节点数量分别为10，20，10，目标的分类3个，并且指定了保存位置
    classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                                hidden_units=[10, 20, 10],
                                                n_classes=2,
                                                model_dir="./DNN_Model")

    # Define the training inputs
    def get_train_inputs():
        x = tf.constant(np.array(sData.astype('float')))
        y = tf.constant(np.array(target))
        return x, y

    # 指定数据，以及训练的步数
    classifier.fit(input_fn=get_train_inputs, steps=2000)

    # 模型评估
    accuracy_score = classifier.evaluate(x=np.array(sData.astype('float')), y=np.array(target))["accuracy"]
    print('Accuracy: {0:f}'.format(accuracy_score))

    # 直接创建数据来进行预测
    # Classify two new flower samples.
    def new_samples():
        return np.array([[3200, 58000, 1], [20, 200, 6]], dtype=np.float32)

    predictions = list(classifier.predict(input_fn=new_samples))
    print("New Samples, Class Predictions:{}".format(predictions))


def classifier(data, time):
    decision_tree = load('decision_tree.model')
    res = decision_tree.predict(data)
    print()
