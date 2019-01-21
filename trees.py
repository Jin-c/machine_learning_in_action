#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author :cj
# date：2018/10/23
from math import log
import operator


def calc_shannon_entropy(dataset):
    """
    计算给定数据集的香农熵
    :param dataset:
    :return:
    """
    num_entries = len(dataset)
    label_counts = {}
    for feat_vec in dataset:
        current_label = feat_vec[-1]
        if current_label not in label_counts.keys():
            label_counts[current_label] = 0
        label_counts[current_label] += 1
    shannon_ent = 0.0
    for key in label_counts:
        prob = float(label_counts[key])/num_entries
        shannon_ent -= prob * log(prob, 2)
    return shannon_ent


def split_dataset(dataset, axis, value):
    """
    按照给定特征划分数据集
    :param dataset:待划分的数据集
    :param axis:划分数据集的特征，特征的第几维
    :param value:需要返回的特征的值
    :return:
    """
    ret_dataset = []
    for feat_vec in dataset:
        if feat_vec[axis] == value:
            reduced_feat_vec = feat_vec[:axis]     # 降维？
            reduced_feat_vec.extend(feat_vec[axis+1:])
            ret_dataset.append(reduced_feat_vec)
    return ret_dataset


def choose_best_feature_to_split(dataset):
    """
    选择最好的数据集划分方式
    :param dataset:
    :return:
    """
    num_features = len(dataset[0]) - 1
    base_entropy = calc_shannon_entropy(dataset)
    best_info_gain = 0.0
    best_feature = -1
    for i in range(num_features):
        feat_list = [example[i] for example in dataset]
        unique_vals = set(feat_list)
        new_entropy = 0.0
        for value in unique_vals:
            sub_dataset = split_dataset(dataset, i, value)
            prob = len(sub_dataset)/float(len(dataset))
            new_entropy += prob * calc_shannon_entropy(sub_dataset)
        info_gain = base_entropy - new_entropy   # 越大越好
        if info_gain > best_info_gain:
            best_info_gain = info_gain
            best_feature = i
    return best_feature


def majority_cnt(class_list):
    """
    对类别计数并从高到低排序，返回出现次数最多的类别
    :param class_list:
    :return:
    """
    class_count = {}
    for vote in class_list:
        if vote not in class_count.keys():
            class_count[vote] = 0
        class_count[vote] += 1
    sorted_class_count = sorted(class_count.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def create_tree(dataset, labels):
    """
    创建决策树，递归算法
    :param dataset:数据集
    :param labels:特征列表
    :return:
    """
    class_list = [example[-1] for example in dataset]
    # 类别完全相同则停止继续划分
    if class_list.count(class_list[0]) == len(class_list):   # list.count(val)  统计val在列表中出现的次数
        return class_list[0]
    # 遍历完所有特征时返回出现次数最多的类别，多数表决方法
    if len(dataset[0]) == 1:
        return majority_cnt(class_list)
    best_feat = choose_best_feature_to_split(dataset)
    best_feat_label = labels[best_feat]
    my_tree = {best_feat_label: {}}
    del(labels[best_feat])
    feat_values = [example[best_feat] for example in dataset]
    unique_vals = set(feat_values)
    # 在每个数据集划分上递归调用函数create_tree()
    for value in unique_vals:
        sub_labels = labels[:]    # 函数参数是列表时，参数按照引用方式传递
        my_tree[best_feat_label][value] = create_tree(split_dataset(dataset, best_feat, value), sub_labels)
    return my_tree


def create_dataset():
    """
    创建数据集
    :return:
    """
    dataset = [
        [1, 1, "yes"],
        [1, 1, "yes"],
        [1, 0, "no"],
        [0, 1, "no"],
        [0, 1, "no"]
    ]
    labels = ["no surfacing", "flippers"]
    return dataset, labels


def retrieve_tree(i):
    """
    输出预先存储的树信息，避免每次测试代码时都要从数据中创建树的麻烦
    :param i:
    :return:
    """
    list_of_tree = [
        {"no surfacing": {0: "no", 1: {"flippers": {0: "no", 1: "yes"}}}},
        {"no surfacing": {0: "no", 1: {"flippers": {0: {"head": {0: "no", 1: "yes"}}, 1: "no"}}}}
    ]
    if i < len(list_of_tree):
        return list_of_tree[i]
    else:
        print("out of index,please input another i-value\n")


def classify(input_tree, feat_labels, test_vec):
    """
    使用决策树的分类函数
    :param input_tree:
    :param feat_labels:
    :param feat_vec:
    :return:
    """
    first_str = list(input_tree.keys())[0]
    second_dict = input_tree[first_str]
    feat_index = feat_labels.index(first_str)
    for key in second_dict.keys():
        if test_vec[feat_index] == key:
            if type(second_dict[key]).__name__ == "dict":
                class_label = classify(second_dict[key], feat_labels, test_vec)
            else:
                class_label = second_dict[key]
    return class_label


if __name__ == "__main__":
    dataset, labels = create_dataset()
    # shannon_ent = calc_shannon_entropy(dataset)
    # print(shannon_ent)
    # trees = split_dataset(dataset, 0, 1)
    # print(trees)
    # best_feature = choose_best_feature_to_split(dataset)
    # print(best_feature)
    my_tree = retrieve_tree(0)
    print(classify(my_tree, labels, [1, 1]))


