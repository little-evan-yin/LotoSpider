import time

import requests
import os

top_dir = "/Users/yindexiang/PycharmProjects/LotoSpider/file/"


def download_pdf(parent_folder, file_name, pdf_url):
    r = requests.get(pdf_url)
    parent_dir = os.path.join(top_dir, parent_folder)
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    with open(os.path.join(parent_dir, file_name), "wb") as f:
        f.write(r.content)


request_url = "http://www.lotoie.com/index.php/index/ajax?act=getFile"
prefix_pdf_url = "http://www.lotoie.com/Public"
headers = {'User-Agent': 'Mozilla/5.0'}

types_dict = {
    '0': 'Announcements',
    '1': 'Financial Reports',
    '2': 'Circulars-Proxy Forms',
    '3': 'Company Information Sheets',
    '4': 'Corporate Governance',
    '5': 'Documents on Display'
}


def get_file_list(type_name, file_type, file_lang):
    page_idx = 1
    has_more = True
    item_count = 0
    while has_more:
        files = {
            'type': (None, file_type),
            'lang': (None, file_lang),
            'page': (None, page_idx)
        }
        response = requests.post(request_url, files=files)
        data_json = response.json()
        if data_json.get('code') < 0:
            # 已经遍历完最后一页
            has_more = False
            tmp_type_list = [type_name] * item_count
            type_list.extend(tmp_type_list)
            break
        data_content = data_json.get('data').get('data')
        for item in data_content:
            title = item.get('f_title')
            pdf_url = prefix_pdf_url + item.get('f_url')
            create_time = item.get('f_create_time')
            download_pdf(file_lang, pdf_url.split('/')[-1], pdf_url)
            date_list.append(create_time)
            title_list.append(title)
            pdf_url_list.append(pdf_url)
            item_count += 1

        page_idx += 1


if __name__ == "__main__":
    lang_list = ['EN', 'CN', 'HK']
    for file_lang in lang_list:
        date_list = []
        title_list = []
        pdf_url_list = []
        type_list = []
        time.sleep(10)
        for i in range(6):
            time.sleep(5)
            type_name = types_dict.get(str(i))
            get_file_list(type_name, i, file_lang)

