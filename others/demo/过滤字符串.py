# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:45
# @Author  : LGD
# @File    : 过滤字符串.py
# @功能    : 过滤字符串


def filter_string(string):
    temp = ''
    str_list = list(string)
    del_list = []
    if len(str_list) <= 1:
        return str_list
    for i in range(len(str_list)):
        if i < len(str_list) - 1:
            if str_list[i] == str_list[i+1]:
                temp = str_list[i]
                del_list.append(i)
                continue
        if temp == str_list[i]:
            del_list.append(i)
    print(del_list)
    del_list.reverse()
    for j in del_list:
        str_list.pop(j)
    str_new = ''.join(str_list)
    print(str_new)
    # return str_new
    for k in range(len(str_new)):
        if k < len(str_new) - 1:
            if str_new[k] == str_new[k+1]:
                filter_string(str_new)
                break
    else:
        print('233')
        return str_new


if __name__ == '__main__':
    temp = 'abbcdddce'
    res = filter_string(temp)
    print(res)




