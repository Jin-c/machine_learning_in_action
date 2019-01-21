#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author :cj
# date：2018/10/24
import matplotlib.pyplot as plt
plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
plt.rcParams["axes.unicode_minus"] = False   # 用来正常显示负号

# 定义文本框和箭头格式
decision_node = dict(boxstyle="sawtooth", fc="0.8")
leaf_node = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")


def plot_node(node_txt, center_pt, parent_pt, node_type):
    """
    使用文本注解绘制树节点
    :param node_txt:
    :param center_pt:
    :param parent_pt:
    :param node_type:
    :return:
    """
    create_plot.axl.annotate(node_txt, xy=parent_pt, xycoords="axes fraction", xytext=center_pt, textcoords="axes fraction",
                            va="center", ha="center", bbox=node_type, arrowprops=arrow_args)


def create_plot(intree):
    """
    创建绘图区，计算树形图的全局尺寸，调用递归函数plot_tree()，注意函数属性的使用
    :param intree:
    :return:
    """
    fig = plt.figure(1, facecolor="white")
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    create_plot.axl = plt.subplot(111, frameon=False, **axprops)   # 绘图区
    plot_tree.totalW = float(get_num_leafs(intree))            # 存储树的宽度
    plot_tree.totalD = float(get_tree_depth(intree))           # 存储树的深度
    # 追踪已经绘制的节点位置，以及放置下一个节点的恰当位置
    plot_tree.xOff = -0.5/plot_tree.totalW
    plot_tree.yOff = 1.0
    plot_tree(intree, (0.5, 1.0), "")
    plt.show()


def get_num_leafs(my_tree):
    """
    获取叶节点的数目，注意递归的使用
    :param my_tree:
    :return:
    """
    num_leafs = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            num_leafs += get_num_leafs(second_dict[key])
        else:
            num_leafs += 1
    return num_leafs


def get_tree_depth(my_tree):
    """
    获取树的层数，注意递归的写法
    :param my_tree:
    :return:
    """
    max_depth = 0
    first_str = list(my_tree.keys())[0]
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            this_depth = 1 + get_tree_depth(second_dict[key])
        else:
            this_depth = 1
        if this_depth > max_depth:
            max_depth = this_depth
    return max_depth


def plot_mid_text(cntr_pt, parent_pt, txt_string):
    """
    计算父节点和子节点的中间位置，并在此处添加文本标签信息
    :param cntr_pt:
    :param parent_pt:
    :param txt_string:
    :return:
    """
    xmid = (parent_pt[0] - cntr_pt[0])/2.0 + cntr_pt[0]
    ymid = (parent_pt[1] - cntr_pt[1])/2.0 + cntr_pt[1]
    create_plot.axl.text(xmid, ymid, txt_string)


def plot_tree(my_tree, parent_pt, node_txt):
    """
    绘制树形图，递归
    :param my_tree:
    :param parent_pt:
    :param node_txt:
    :return:
    """
    # 计算宽与高
    num_leafs = get_num_leafs(my_tree)
    depth = get_tree_depth(my_tree)
    first_str = list(my_tree.keys())[0]
    cntr_pt = (plot_tree.xOff + (1.0 + float(num_leafs))/2.0/plot_tree.totalW, plot_tree.yOff)
    # 标记子节点属性值
    plot_mid_text(cntr_pt, parent_pt, node_txt)
    plot_node(first_str, cntr_pt, parent_pt, decision_node)
    # 减少y偏移
    plot_tree.yOff = plot_tree.yOff - 1.0/plot_tree.totalD
    second_dict = my_tree[first_str]
    for key in second_dict.keys():
        if type(second_dict[key]).__name__ == "dict":
            plot_tree(second_dict[key], cntr_pt, str(key))
        else:
            plot_tree.xOff = plot_tree.xOff + 1.0/plot_tree.totalW
            plot_node(second_dict[key], (plot_tree.xOff, plot_tree.yOff), cntr_pt, leaf_node)
            plot_mid_text((plot_tree.xOff, plot_tree.yOff), cntr_pt, str(key))
    plot_tree.yOff = plot_tree.yOff + 1.0/plot_tree.totalD


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


if __name__ == "__main__":
    # create_plot()
    my_tree = retrieve_tree(0)
    # print(get_num_leafs(my_tree))
    # print(get_tree_depth(my_tree))
    create_plot(my_tree)
