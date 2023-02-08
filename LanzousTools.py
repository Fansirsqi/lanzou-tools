# _*_coding:utf-8_*_

# @PROJECT : lanzou-tools
# @Time : 2023/2/8 11:10
# @Author : Byseven
# @File : LanzousTools.py
# @SoftWare:
import Lanzous
import random
import string
import pandas as pd


def table(data: list):
    """处理函数generate_form返回的数据，写入表格"""
    soft_table_title = ['SOFTNAME', 'SHARELINK', 'SIZE', 'PASSWORD']
    folder_table_title = ['FOLDERNAME', 'SHARELINK', 'PASSWORD', 'DESC']
    pd_soft = pd.DataFrame(data[0], columns=soft_table_title)
    pd_soft.to_excel('lanzou_download.xlsx', index=False, sheet_name='soft-list')
    writer = pd.ExcelWriter(r'lanzou_download.xlsx', mode='a', engine='openpyxl')
    pd_folder = pd.DataFrame(data[1], columns=folder_table_title)
    pd_folder.to_excel(writer, index=False, sheet_name='folder-list')
    writer.save()
    writer.close()
    print('excel写入完毕')


def list_to_str(ls):
    """列表转字符串"""
    return ''.join(ls)


def set_vei(n: int):
    """返回n位随机字符串，不包含特殊字符"""
    num = '1234567890'
    a_str = list_to_str(list(string.ascii_lowercase))
    A_str = list_to_str(list(string.ascii_uppercase))
    all_str = a_str + num + A_str
    vei = ''
    for key in range(n):
        key = random.choice(all_str)
        vei = ''.join([vei, key])
    return vei
