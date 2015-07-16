#!/usr/bin/env python
# -*- coding: gbk -*-

__author__ = 'patson'
import sys

# ����·��
project_path = sys.path[0] + '\\'

# �����ļ�����
properties_name = 'post_urls.properties'

# ����ͼƬ�洢��·��
post_images_pardir = 'pictures\\'

# ������URL�����ҳ��
url_suffix = '&page='

# ͼƬ������ַ
img_link_prefix = 'http://img.nga.cn/attachments'

# ��ȡͼƬ��Ե�ַ������
img_link_pattern = r',url:\'(.*?)\',name:'

# ��ȡͼƬ��ַ�����Ƶ�����
img_link_and_name_pattern = r',url:\'(.*?)\',name:\'(.*?)\''

# ��ȡ�������Ƶ����������ļ�������
post_title_pattern = r'<title>(.*?)</title>'

# ��ȡ������ҳ������
post_page_num_pattern = r',1:([0-9]*?),'

