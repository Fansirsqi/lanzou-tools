import requests

import LanzousTools


class Lanzou:
    uid = '454001'  # uid请填入
    fid = '-1'  # fid 默认-1
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        'content-length': '50',
        'cookie': f'ylogin={uid}; folder_id_c={fid}; _uab_collina=166719911702083626287627; PHPSESSID=bslpegm0kl88om0jmuhoius968e1cpcd; uag=98d0592cda8050aaec088d732be8be1b; phpdisk_info=UGBSZQ1rUW0PPQBhD1xVOwJbAXsBMVxzD2VXYlImAQpVNFQwVTZRZAJkAjMKY1M6UDVQMF5hUjEONAlqAGcKalBmUmINbVFvDz0AMQ9jVTYCNgFiATlcbQ9uV2ZSMgE2VVhUZ1U%2FUW8CNwJrCmVTOlAzUGdeN1Ix',
        'origin': 'https://pc.woozooo.com',
        'pragma': 'no-cache',
        'referer': f'https://pc.woozooo.com/mydisk.php?item=files&action=index&u={uid}',
        'sec-ch-ua': '"Microsoft Edge";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.52',
        'x-requested-with': 'XMLHttpRequest',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }

    def exc_index_fold(self):
        """获取首页资源"""
        index_url = f'https://pc.woozooo.com/doupload.php?uid={self.uid}'
        fopayload = f'task=47&folder_id=-1&vei={LanzousTools.set_vei(16)}'
        fores = requests.post(url=index_url, headers=self.headers, data=fopayload).json()
        # print(fores) 文件夹返回
        fepayload = f'task=5&folder_id=-1&pg=1&vei={LanzousTools.set_vei(16)}'
        feres = requests.post(url=index_url, headers=self.headers, data=fepayload).json()
        # print(feres)  文件返回
        return [fores, feres]

    def get_folder_all_info(self, fid: str):
        """获取文件夹，以及下级文件"""
        index_url = f'https://pc.woozooo.com/doupload.php?uid={self.uid}'
        fopayload = f'task=47&folder_id={fid}&vei={LanzousTools.set_vei(16)}'
        fores = requests.post(url=index_url, headers=self.headers, data=fopayload).json()
        # print(fores)
        fepayload = f'task=5&folder_id={fid}&pg=1&vei={LanzousTools.set_vei(16)}'
        feres = requests.post(url=index_url, headers=self.headers, data=fepayload).json()
        # print(feres)
        return [fores, feres]

    def get_index_folder_id(self):
        """获取首页文件夹id"""
        ls = []
        dic = self.exc_index_fold()[0]
        for i in dic['text']:
            ls.append(i['fol_id'])
        return ls

    def get_index_file_info(self):
        """获取首页文件信息"""
        ls = []
        dic = self.exc_index_fold()[1]
        for item in dic['text']:
            ls.append({'name': item['name_all'],
                       'id': item['id'],
                       'size': item['size'],
                       'tpe': 'file'})
        return ls

    def get_share_link(self, tpe: str, id: str):
        """获取分享链接"""
        # tpe = 'file/folder'
        if tpe == 'file':
            tsk = '22'
        elif tpe == 'folder':
            tsk = '18'
        else:
            print('传入类型异常')
            exit()
        url = 'https://pc.woozooo.com/doupload.php'
        payload = f'task={tsk}&{tpe}_id={id}'
        res = requests.post(url=url, headers=self.headers, data=payload).json()['info']
        if tpe == 'folder':
            return [res['name'], res['new_url'], res['pwd'], res['des']]
        elif tpe == 'file':
            return res['is_newd'] + '/' + res['f_id'], res['pwd']

    def get_this_folder_all_file_info(self, dic: list):
        """获取当前文件夹下所有文件信息"""
        ls = []
        for item in dic[1]['text']:
            ls.append({'name': item['name_all'],
                       'id': item['id'],
                       'size': item['size'],
                       'tpe': 'file'})
        return ls

    def get_this_folder_all_folder_id(self, dic: list):
        """
        :param dic: [dict,dict](res)传入上个函数返回的数据即可
        :return:
        """
        ls = []
        for i in dic[0]['text']:
            ls.append(i['fol_id'])
        return ls

    def get_all_file_info(self):
        """获取所有文件信息"""
        index_file_info = self.get_index_file_info()
        all_folder_ids = self.get_all_folder_id()
        all_file_info = []
        for fid in all_folder_ids:
            item_folder_list = self.get_folder_all_info(fid)  # 根据所有文件夹id 获取所有文件的info_list
            all_file_info = self.get_this_folder_all_file_info(item_folder_list) + all_file_info
        all_file_info = index_file_info + all_file_info
        return all_file_info

    def get_all_folder_id(self):
        """获取所有文件夹id"""
        index_folder_ids = self.get_index_folder_id()
        all_folder_ids = []
        for fid in index_folder_ids:
            item_folder_list = self.get_folder_all_info(fid)  # 这里直接拿到文件夹id去解析有无子目录，有的话则添加进列表，避免遗漏
            all_folder_ids = self.get_this_folder_all_folder_id(item_folder_list) + all_folder_ids
        all_folder_ids = index_folder_ids + all_folder_ids
        return all_folder_ids

    def generate_form(self):
        soft_list = self.get_all_file_info()
        for i in soft_list:
            link, pwd = self.get_share_link(i['tpe'], i['id'])
            i.update({
                'sharelink': link,
                'pwd': pwd
            })
        # 文件列表
        ex_data = []
        for j in soft_list:
            ex_data.append([j['name'], j['sharelink'], j['size'], j['pwd']])
        # 文件夹
        all_fid = self.get_all_folder_id()
        wl = []
        for i in all_fid:
            wl.append(self.get_share_link('folder', i))
        return [ex_data, wl]
