from sklearn.tree import DecisionTreeClassifier, tree
from sklearn.tree.export import export_graphviz
import tensorflow as tf
from tensorflow import keras
from joblib import dump, load
import pickle


def classifierTraining(data, sData, time, target, colName):
    decision_tree = DecisionTreeClassifier(random_state=0, max_depth=2)
    decision_tree = decision_tree.fit(sData, target)
    dump(decision_tree, 'decision_tree.model')


def DNNclassiferTraining(data, sData, time, target, colName):
    # 每行数据3个特征，都是real-value的
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=3)]

    # 构建一个DNN分类器，3层，其中每个隐含层的节点数量分别为10，20，10，目标的分类3个，并且指定了保存位置
    classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                                hidden_units=[10, 20, 10],
                                                n_classes=2,
                                                model_dir="/DNN_Model")
    # 指定数据，以及训练的步数
    classifier.fit(x=sData, y=target, steps=2000)

def classifier(sData, time):
    decision_tree = load('decision_tree.model')
    decision_tree.predict(sData)
    print()