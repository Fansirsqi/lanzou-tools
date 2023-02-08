# _*_coding:utf-8_*_

# @PROJECT : lanzou-tools
# @Time : 2023/2/8 11:12
# @Author : Byseven
# @File : mian.py
# @SoftWare:

import Lanzous,LanzousTools

if __name__ == '__main__':
    obj = Lanzous.Lanzou()
    data = obj.generate_form()
    LanzousTools.table(data)
