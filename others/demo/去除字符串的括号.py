# -*- coding: utf-8 -*-
# @Time    : 2019/10/7 11:03
# @Author  : LGD
# @File    : 去除字符串的括号.py
# @功能    : 去除string的每个独立的外部括号，返回每个独立括号的string


def DeleteBrackets(is_str):
    """
    去除多层括号的最外层，返回内层括号
    使用tag作为计数变量，表示当前括号层数，
    当层数为零时跳出循环，返回当前括号的内层字符串
    :param is_str:
    :return:
    """
    str1 = is_str
    result = ''
    str_len = len(str1)

    for i in range(str_len):
        if str1[i] == '(':          # 遇到左括号进入判断
            tag = 1                 # tag标为1
            stack = []              # 用list作为栈，遍历到的元素依次压栈

            for j in range(i + 1, str_len):
                stack.append(str1[j])           # 压栈
                if str1[j] == ')' and tag:
                    tag -= 1                    # 遇到右括号括号层数减1
                if str1[j] == '(' and tag:
                    tag += 1                    # 遇到左括号括号层数加1
                if tag == 0:                    # 层数为0 跳出循环
                    stack.pop()                 # 去除最外层循环，所以丢弃最后一个右括号
                    for k in stack:
                        result += k             # 将列表拼接成字符串输出
                    break
    return result


if __name__ == "__main__":
    string = '(())()'
    res = DeleteBrackets(string)
    print(res)












