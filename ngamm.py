#!/usr/bin/env python
# -*- coding: gbk -*-

__author__ = 'Administrator'

import re
import requests
import os
import urllib
import nga_headers_cookies
import setting
import utils
import time
from utils import print_log


# TODO: 1������� 2����־װ����

def main():
    try:
        urls = utils.get_urls_from_txt_file(setting.urls_file_name)
    except IOError:
        print '�����ļ������ڻ�û�д�����ĵ�ַ'
    else:
        for url in urls:
            try:
                let_us_go(url)
            except IOError, e:
                print e
                break


def let_us_go(url):
    try:
        print '\n\n'
        # �������Դ��
        post_content = get_url_content(url)
        if not post_content:
            raise IOError('%s ���ݻ�ȡʧ�ܣ��������״̬' % url)
        # ������ӱ���
        post_image_dir_name = dry_nga_title(get_post_title(post_content))
        print '���� : %s' % post_image_dir_name
        # �������ҳ��
        post_pages = get_post_total_pages(post_content)
        print 'ҳ�� : %s' % post_pages
        # ��������ͼƬ�ļ���
        img_path = make_post_image_dir(post_image_dir_name)
        print 'ͼƬ���Ŀ¼�� : %s' % img_path
        # ������������ӵ�txt�ļ���
        record_file_name = img_path + post_image_dir_name + '.txt'
        # �����������ͼƬhttp·��
        img_links = fetch_post_image_links(url, post_pages)
        # ɾ���Ѿ����ع���ͼƬ����
        print_log('��ʼɾ���ظ�����')
        new_img_links = remove_repeat_img_links(record_file_name, img_links)
        print_log('ɾ���ظ��������')
        print '����ͼƬ��: %s' % len(new_img_links)
        # ����ͼƬ
        download_images_from_link_list(new_img_links, img_path, record_file_name)
    except IOError, e:
        print e


def get_url_content(url):
    response = requests.get(url, headers=nga_headers_cookies.headers, cookies=nga_headers_cookies.cookies())
    if response.status_code != 200:
        print 'Request (%s)\'s false,status_code = %s' % (url, response.status_code)
        return ''
    else:
        return response.content


def get_post_title(content):
    reg = re.compile(setting.post_title_pattern)
    title = re.findall(reg, content)
    return title[0] if title else 'default'


def dry_nga_title(nga_post_title):
    return nga_post_title if nga_post_title.find('������˹���ҵ�����̳') == -1 \
        else nga_post_title[:nga_post_title.rfind('������˹���ҵ�����̳') - 3]


def get_post_total_pages(content):
    reg = re.compile(setting.post_page_num_pattern)
    pages_num = re.findall(reg, content)
    return int(pages_num[0]) if pages_num else 1


def fetch_post_image_links(url, post_pages):
    print_log('��ʼ�ռ�����ȫ��ͼƬ����')
    post_content_reg = re.compile(setting.post_content_pattern, re.S)
    link_reg = re.compile(setting.img_link_pattern)
    link_reg2 = re.compile(setting.img_link_with_third_site_pattern)
    img_links = []
    for page in range(1, post_pages + 1):
        print '��ǰҳ��:%s\r' % page,
        curl_page_url = utils.make_url_with_page_num(url, page)
        whole_content = get_url_content(curl_page_url)
        if whole_content:
            content = (re.findall(post_content_reg, whole_content))[0]
            origin_img_links = re.findall(link_reg, content) + re.findall(link_reg2, content)
            img_links += [utils.make_real_img_link(link) for link in origin_img_links]
    print_log('�ռ��������')
    return sorted(utils.clean_str_list(img_links))


def remove_repeat_img_links(record_file_name, img_links):
    if os.path.exists(record_file_name):
        download_records_file = open(record_file_name, 'r+')
        # ���ع���ͼƬ����
        existed_links = utils.clean_str_list(download_records_file.readlines())
        # �������ӣ��������Ӽ�ȥ���������ӣ�
        new_links = sorted(list(set(img_links) - set(existed_links)))
        # ����������׷��д������¼�ļ� ����������Ϊ�º�һ�Ŵ�һ�ŵĵ�ַ��
        # download_records_file.writelines([link + '\n' for link in new_links])
        download_records_file.close()
        return new_links
    else:
        # download_records_file = open(record_file_path, 'w')
        # download_records_file.writelines([link + '\n' for link in img_links])
        # download_records_file.close()
        return img_links


def make_post_image_dir(post_image_dir_name):
    """���ɴ������ͼƬ���ļ���.
    :param post_image_dir_name:�ļ�������
    :return �ļ�������·��
    """
    # ���� pictures �ļ���
    parent_dir = setting.project_path + setting.post_images_pardir
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    # ���������ļ���
    real_dir = parent_dir + post_image_dir_name
    if not os.path.exists(real_dir):
        os.mkdir(real_dir)
    return real_dir + '\\'


def download_images_from_link_list(img_links, img_path, record_file_name):
    print_log('��������ͼƬ��')
    start_time = time.time()
    total = len(img_links)
    record_file = open(record_file_name,'a')
    for index, link in enumerate(img_links):
        print_log('�� %s / %s ��' % (str(index + 1), total))
        urllib.urlretrieve(link, filename=img_path + '\\' + utils.clean_filename(link[link.rfind('/') + 1:]),
                           reporthook=schedule)
        record_file.write(link + '\n')
    end_time = time.time()
    record_file.close()
    print_log('��������ͼƬ������ : %s �� ' % str(round(end_time - start_time, 2)))


def schedule(a, b, c):
    """���ؽ���
    a:�Ѿ����ص����ݿ�
    b:���ݿ�Ĵ�С
    c:Զ���ļ��Ĵ�С
    """
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%\r' % per,


if __name__ == '__main__':
    main()
