# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/15
# Desc：不过是大梦一场空，不过是孤影照惊鸿。

import json
import os


def MakeSureDirExist(path):
	# 确保文件存在
	if not os.path.exists(path):
		path_dir = os.path.dirname(path)
		if not os.path.exists(path_dir):
			os.makedirs(path_dir)
		
		with open(path, "a", encoding="utf-8") as f:
			json.dump({}, f, ensure_ascii=False, indent=4)


def LoadJson(path):
	# 读取json文件
	try:
		MakeSureDirExist(path)
		with open(path, "r", encoding="utf-8") as f:
			data = json.load(f)
	except:
		print("读取文件:", path, "失败")
		data = {}
	return data


def SaveJson(path, data):
	# 保存json文件
	MakeSureDirExist(path)
	with open(path, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=4)
