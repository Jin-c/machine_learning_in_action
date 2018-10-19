#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author :cj
# date：2018/10/17
from numpy import *
from os import listdir
from kNN_dating import classify0


def img2vector(filename):
    """将图像（文本格式）转换为向量"""
    return_vect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        line_str = fr.readline()
        for j in range(32):
            return_vect[0, 32*i+j] = int(line_str[j])
    return return_vect


def hand_writing_class_test():
    """手写数字识别系统的测试代码"""
    hw_labels = []
    training_file_list = listdir("./data/digits/trainingDigits")
    m = len(training_file_list)
    training_mat = zeros((m, 1024))
    for i in range(m):
        filename = training_file_list[i]
        filestr = filename.split(".")[0]
        class_num = int(filestr.split("_")[0])
        hw_labels.append(class_num)
        training_mat[i:] = img2vector("./data/digits/trainingDigits/%s" % filename)
    test_file_list = listdir("./data/digits/testDigits")
    error_count = 0.0
    m_test = len(test_file_list)
    for i in range(m_test):
        filename = test_file_list[i]
        filestr = filename.split(".")[0]
        class_num = int(filestr.split("_")[0])
        vector_under_test = img2vector("./data/digits/testDigits/%s" % filename)
        classifier_result = classify0(vector_under_test, training_mat, hw_labels, 3)
        if classifier_result != class_num:
            error_count += 1.0
    print("the total number of errors is: %d\n" % error_count)
    print("the total error rate is: %f\n" % (error_count/float(m_test)))


if __name__ == "__main__":
    # test_vector = img2vector("./data/digits/testDigits/0_13.txt")
    # print(test_vector)
    hand_writing_class_test()
