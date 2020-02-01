# -*- coding:utf-8 -*-
# @Author : 'LZ'
# @Time : 2019/12/7 15:59

from hashlib import md5


def gen_md5(args):
	ha = md5(b'salt')   # 加盐字节形式
	ha.update(args.encode('utf-8'))   # 将数据转为字节再加密
	return ha.hexdigest()



































