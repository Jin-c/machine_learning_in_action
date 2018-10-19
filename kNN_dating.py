#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author :cj
# date：2018/10/17
from numpy import *
import operator
import matplotlib
import matplotlib.pyplot as plt


def create_data_set():
    """创建数据和标签"""
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ["A", "A", "B", "B"]
    return group, labels


def classify0(inX, data_set, labels, k):
    """k-近邻算法，返回inX的分类label"""
    data_set_size = data_set.shape[0]    # array.shape = (行数，列数)
    diff_mat = tile(inX, (data_set_size, 1)) - data_set   # tile(A, B) 重复A B次,B = (行数=1，列数)
    sq_diff_mat = diff_mat ** 2       # array**2:各个位置的元素的平方，不会内积
    sq_distances = sq_diff_mat.sum(axis=1)   # 0：按列相加，1：按行相加
    distances = sq_distances ** 0.5
    sorted_dist_indicies = distances.argsort()    # 数组值从小到大的索引值
    class_count = {}
    for i in range(k):
        vote_i_label = labels[sorted_dist_indicies[i]]
        class_count[vote_i_label] = class_count.get(vote_i_label, 0) + 1   # dict.get()
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)  # operator.itemgetter()
                                                                                                # 用于获取对象的哪些维的数据
    # print(sorted_class_count)
    return sorted_class_count[0][0]


def file2matrix(filename):
    """将文本记录转换为numpy，输出为训练样本矩阵和类标签向量"""
    fr = open(filename)
    array_lines = fr.readlines()
    number_lines = len(array_lines)
    return_mat = zeros((number_lines, 3))  # zeros() 创建任意维度的数组，数据类型默认是浮点型，可指定
    class_label_vector = []
    index = 0
    for line in array_lines:
        line = line.strip()
        list_from_line = line.split("\t")
        return_mat[index, :] = list_from_line[0:3]   # 特征，注意数组切片操作
        class_label_vector.append(int(list_from_line[-1]))  # 标签
        index += 1
    return return_mat, class_label_vector


def mat_show(xdata, ydata, labels=[]):
    """用matplotlib制作散点图"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # ax.scatter(xdata, ydata)
    ax.scatter(xdata, ydata, 15.0 * array(labels), 15.0 * array(labels))  # 大小，颜色
    plt.show()


def auto_norm(data_set):
    """归一化特征值***将数字特征值转化为0到1的区间，返回归一化矩阵，取值范围，最小值"""
    min_vals = data_set.min(0)     # 0:每列的最小值，1:每行的最小值
    max_vals = data_set.max(0)
    ranges = max_vals - min_vals
    norm_data_set = zeros(shape(data_set))
    m = data_set.shape[0]         # 行数
    norm_data_set = data_set - tile(min_vals, (m, 1))
    norm_data_set = norm_data_set/tile(ranges, (m, 1))     # array除法，对应位置相除
    return norm_data_set, ranges, min_vals


def dating_class_test():
    """分类器针对约会网站的测试代码"""
    ho_ratio = 0.10
    dating_data_mat, dating_labels = file2matrix("./data/datingTestSet2.txt")
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    m = norm_mat.shape[0]
    num_test_vecs = int(m*ho_ratio)     # 测试数据的行数
    error_count = 0.0
    for i in range(num_test_vecs):
        classifier_result = classify0(norm_mat[i, :], norm_mat[num_test_vecs:m, :], dating_labels[num_test_vecs:m], 3)
        # print("the classifier came back with: %d, the real answer is: %d" % (classifier_result, dating_labels[i]))
        if classifier_result != dating_labels[i]:
            error_count += 1.0
    print("the total error rate is: %f" % (error_count/float(num_test_vecs)))


def classify_person():
    """约会网站预测函数，用户输入特征，输出person相应的标签，输入示例：10,10000,0.5"""
    result_list = ["not at all", "in small doses", "in large doses"]
    percent_tats = float(input("percentage of time spent playing video games? "))
    ff_miles = float(input("frequent flier miles earned per year? "))
    ice_cream = float(input("liters of ice cream consumed per year? "))
    dating_data_mat, dating_labels = file2matrix("./data/datingTestSet2.txt")
    norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    in_arr = array([ff_miles, percent_tats, ice_cream])
    classifier_result = classify0((in_arr - min_vals)/ranges, norm_mat, dating_labels, 3)
    print("You will probably like this person: %s" % result_list[classifier_result - 1])


if __name__ == "__main__":
    # group, labels = create_data_set()
    # print(classify0([1, 1], group, labels, 3))
    # dating_data_mat, dating_labels = file2matrix("./data/datingTestSet2.txt")
    # mat_show(dating_data_mat[:, 1], dating_data_mat[:, 2], dating_labels)
    # mat_show(dating_data_mat[:, 0], dating_data_mat[:, 1], dating_labels)
    # norm_mat, ranges, min_vals = auto_norm(dating_data_mat)
    # print(norm_mat)
    # print(ranges)
    # print(min_vals)
    dating_class_test()
    classify_person()
