from sklearn.tree import DecisionTreeClassifier, tree
from sklearn.tree.export import export_graphviz
import tensorflow as tf
from tensorflow import keras
import numpy as np
from joblib import dump, load
from sklearn.tree.export import export_text
from sklearn.metrics import accuracy_score


def skDecisionTreeTrain(data, fdata, sdata, time, target, colname):
    decision_tree = DecisionTreeClassifier(random_state=1, max_depth=10)

    decision_tree = decision_tree.fit(fdata, target)
    dump(decision_tree, 'decision_tree.model')
    sCol = ["view", "size", "subsets", "created", "updated"]
    r = export_text(decision_tree, feature_names=sCol)
    print(r)
    predict = decision_tree.predict(fdata)
    print(accuracy_score(target, predict))


def tfDNNClassiferTrain(data, fdata, sdata, time, target, colName):
    # 每行数据3个特征，都是real-value的
    # feature_columns = [tf.contrib.layers.real_valued_column("", dimension=3)]
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=5)]

    # 构建一个DNN分类器，3层，其中每个隐含层的节点数量分别为100，200，100，目标的分类2个，并且指定了保存位置
    dnnclf = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20, 10],
                                            n_classes=2,
                                            model_dir="./DNN_Model")

    # Define the training inputs
    def get_train_inputs():
        # x = tf.constant(sData)
        x = tf.constant(fdata)
        y = tf.constant(target)
        return x, y

    # 指定数据，以及训练的步数
    dnnclf.fit(input_fn=get_train_inputs, steps=20000)

    # 模型评估
    accuracy_score = dnnclf.evaluate(x=fdata, y=target)["accuracy"]
    print('Accuracy: {0:f}'.format(accuracy_score))

    # # 直接创建数据来进行预测
    # # Classify two new flower samples.
    # def new_samples():
    #     return np.array([[3200, 58000, 1], [20, 200, 6]], dtype=np.float32)
    #
    # predictions = list(dnnclf.predict(input_fn=new_samples))
    # print("New Samples, Class Predictions:{}".format(predictions))


def tfLinearClassifierTrain(data, fdata, sdata, time, target, colname):
    # feature_columns = tf.contrib.learn.infer_real_valued_columns_from_input(X_train)
    feature_columns = [tf.contrib.layers.real_valued_column("", dimension=3)]
    linclf = tf.contrib.learn.LinearClassifier(feature_columns=feature_columns,
                                               n_classes=2,
                                               model_dir="./Linear_Model")

    # Define the training inputs
    def get_train_inputs():
        x = tf.constant(fdata)
        y = tf.constant(target)
        return x, y

    # 指定数据，以及训练的步数
    linclf.fit(input_fn=get_train_inputs, steps=20000)

    # 模型评估
    accuracy_score = linclf.evaluate(x=fdata, y=target)["accuracy"]
    print('Accuracy: {0:f}'.format(accuracy_score))


def classifier(data, model):
    if model == 'dt':
        curmodel = load('decision_tree.model')
        res = curmodel.predict(data)
        print (res)
    elif model == 'dnn':
        with tf.Session() as sess:
            new_saver = tf.train.import_meta_graph('classifier/DNN_Model/model.ckpt-20000.meta')
            new_saver.restore(sess, 'classifier/DNN_Model/model.ckpt-20000.data-00000-of-00001')
            # tf.get_collection() 返回一个list. 但是这里只要第一个参数即可
            y = tf.get_collection('pred_network')[0]

            graph = tf.get_default_graph()

            # 因为y中有placeholder，所以sess.run(y)的时候还需要用实际待预测的样本以及相应的参数来填充这些placeholder，而这些需要通过graph的get_operation_by_name方法来获取。
            input_x = graph.get_operation_by_name('input_x').outputs[0]
            keep_prob = graph.get_operation_by_name('keep_prob').outputs[0]

            # 使用y进行预测
            res = list(sess.run(y, feed_dict={input_x: data, keep_prob: 1.0}))

    print(res)
