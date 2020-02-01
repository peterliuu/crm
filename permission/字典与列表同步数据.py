import copy
menu_list = [
	{"id": 1, "title": "客户列表"},
	{"id": 2, "title": "用户列表"},
]


menu_dic = {}

for item in menu_list:
	menu_dic[item["id"]] = item

# 更新字典中的value值，list中的数据是否会改变？--》
# 会改变，因为列表中的数据和字典中的value使用的是同一块内存地址

for key, value in menu_dic.items():
	value["children"] = "666"

print(menu_dic)
print(menu_list)

# 如何使得改变字典中的value值，list中的数据不改变
# 深拷贝
menu_dic = copy.deepcopy(menu_dic)

for key, value in menu_dic.items():
	value["children"] = "777"

print(menu_dic)
print(menu_list)


