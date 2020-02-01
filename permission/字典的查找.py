# 请判断id为1的元素在列表中是否存在
# 请判断id为2的元素在列表中是否存在
menu_list = [
	{"id": 1, "title": "客户列表"},
	{"id": 2, "title": "用户列表"},
]

# 正常思路--循环查询
for item in menu_list:
	for key, value in item.items():
		if key == "id" and value == 1:
			print("找到啦")

# 但是查询多次需要多次循环
# 转化数据结构
menu_dict = {}
for item in menu_list:
	menu_dict[item["id"]] = item
	
'''
{1: {'id': 1, 'title': '客户列表'},
 2: {'id': 2, 'title': '用户列表'}
 }
'''

# 直接判断：
if 1 in menu_dict.keys():
	pass





