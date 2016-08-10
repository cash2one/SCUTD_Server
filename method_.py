#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeperfect
# @Date:   2016-02-28 13:10:20
# @Last Modified by:   leeperfect
# @Last Modified time: 2016-03-06 00:10:46
import leancloud
from werkzeug import secure_filename
from leancloud import Query,Object,User,LeanCloudError,File
import time,json


import sys
reload(sys)
sys.setdefaultencoding('utf-8')



leancloud.init(APP_ID, master_key=MASTER_KEY)

# ================一些公开的function===========


def query_db(db_name):
	db_object = Object.extend(db_name)
	db_query = Query(db_object)
	return db_query


def init_db(db_name):
	db_object = Object.extend(db_name)
	db = db_object()
	return db

# ================公开的function结束===========

class magazine_tools(object):
	"""docstring for magazine_tools"""
	



class user_tools(object):
	"""docstring for user_tools"""
	def down_user_by_title(self,title,magazine,index_):
		try:
			user_list = query_db("magazine").equal_to("title",int(title)).equal_to("magazine",int(magazine)).first().get("user_list")
			user_obj = user_list.split("-")[int(index_)-1]
			user_info = query_db("user_db").get(user_obj)
			user_info.set("stat",2)
			user_info.save()
			return json.dumps({"success":"success"})
		except Exception,e:
			print "已上架用户下架模块出现问题,问题报告如下"
			print e
			print "发生问题期数: ",str(title),"第: ",str(index_),"个用户,来自: ",str(magazine)
			print "-------"*15
			
			return json.dumps({"success":"failed"})
	def down_user_unpublished(self,wechat_id):
		
		user = query_db("user_db").equal_to("contact_normal",wechat_id).find()
		try:
			if user:
				user = user[0]
				user.set("stat",2)
				user.save()
				return json.dumps({"success":"success"})
			else:

				return json.dumps({"success":"none"})
		except Exception,e:
			print "未上架用户下架模块出现问题,问题报告如下"
			print e
			print "发生问题用户微信号为: ",str(wechat_id)
			print "-------"*15

			return json.dumps({"success":"failed"})















		