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

# ������������(python����ͨ��� . ���������з�����Ҫƥ�任�з���re.complie������������������re.S��
# re.S�������ƥ�䣡�����������ˣ�����)
post_content_pattern = r'<div id=\'m_nav\' class=\'module_wrap\'>(.*?)<div class=\'module_wrap\'>'

# ��ȡͼƬ��Ե�ַ������
img_link_pattern = r',url:\'(.*?)\',name:'

# ��ȡ������ͼƬ��ַ������
img_link_with_third_site_pattern = r'\[img\](.*?)\[/img\]'

# ��ȡͼƬ��ַ�����Ƶ�����
img_link_and_name_pattern = r',url:\'(.*?)\',name:\'(.*?)\''

# ��ȡ�������Ƶ����������ļ�������
post_title_pattern = r'<title>(.*?)</title>'

# ��ȡ������ҳ������
post_page_num_pattern = r',1:([0-9]*?),'
