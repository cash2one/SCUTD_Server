#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeperfect
# @Date:   2015-09-04 00:38:13
# @Last Modified by:   leeperfect
# @Last Modified time: 2016-03-05 20:09:54

import leancloud
# from StringIO import StringIO
import codecs
from werkzeug import secure_filename
from cStringIO import StringIO
from leancloud import Query,Object,User,LeanCloudError,File
import time,json
import requests
from PIL import Image
from tools import *


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



class read_leancloud:
	

	def get_user_info(self,page,publish_type):
		page = page-1
		user_query = query_db("user_db").include("user_photo").include("user_card_photo").include("school_id").equal_to("stat",0)
		if publish_type == "0":
			user_query.not_contained_in("public_type",[1])
		else:
			user_query.equal_to("public_type",int(publish_type))
		user_query = user_query.skip(int(page)*30).equal_to("sex","男神").limit(999).ascending("createdAt").find()+user_query.skip(int(page)*30).equal_to("sex","女神").limit(999).ascending("createdAt").find()
		
		user_list = {"boy":[],"girl":[]}

		for x in user_query:
			info_wanted = ["prefer","hobbies","contact_normal",'hometown','height','nick_name','age','school']
			user_piece = {}
			for info_name in info_wanted:
				user_piece[info_name] = x.get(info_name)
			user_piece["photo"] = x.get("user_photo").url
			user_piece["card_photo"] = x.get("user_card_photo").url
			user_piece["objectId"] =x.id
			if x.get("sex") == u"男神":
				user_list["boy"].append(user_piece)
			elif x.get("sex") == u"女神":
				user_list["girl"].append(user_piece)
		



		return user_list

	def get_file_url_by_id(self,objid):
		"通过photo的objectid获取photo的File对象"
		db_object = query_db("_File")
		try:
			photo_url = db_object.get(objid).get("url")
		except:
			photo_url = ""

		photo_url += '?imageView/0/w/600/h/1200'  
		return photo_url

	
	

	def get_magazine(self,page,publish_type):
		db = query_db("magazine").equal_to("title",int(page)).equal_to("magazine",int(publish_type)).first()
		user_list = db.get("user_list").split("-")
		re = []
		for x in user_list:
			people = Object.dump(query_db("user_db").get(x))
			img_url = read_leancloud().get_file_url_by_id(people["photo"][0])
			people["photo"] = img_url
			re.append(people)
		return re


	
	def get_object(self,db_name,objid):
		"通用接口,用来通过objectId获取某个表中定向数据"
		try:
			db = query_db(db_name).get(objid)
			re_dict = Object.dump(db)
			return re_dict
		except:
			return {}

	def get_admin(self,user_name,user_pass):
		try:
			User().login(user_name,user_pass)
			user_query = query_db("_User").equal_to("username",user_name).first()
			objid = str(user_query.id)
			return objid
		except Exception,e:
			print e
			return ""

	def find_lc_one(self,db_name,arr):
		db_ = query_db(db_name)
		try:
			for x in arr:
				db_.equal_to(x,arr[x].encode("utf-8"))
			re = Object.dump(db_.first()) 
			
			return json.dumps(re)
		except:
			return ""

	def get_title_list(self,magazine):
		re_ = query_db("magazine").equal_to("magazine",int(magazine)).descending("title").limit(200).find()
		re_ = [x.get("title") for x in re_]
		return re_





class write_leancloud:


	def del_user_by_objid(self,obj):
		img_to_del = query_db("user_db").get(obj)
		img_to_del.set("stat",3).save()

		return True

	# ======通用类=====
	def change(self,db_name,objid,content):
		"统一的接口用来以objectId搜索并改变其中内容"
		db = query_db(db_name).get(objid)
		for x in content:


			db.set(x,content[x])
		db.save()
		return db
	def change_school_type(self):
		"用来  定时任务  中批量切换不同报名者学校的school_type"
		school_list = ["其他","四川大学","电子科大","西南财经","西南民族","四川音乐","四川师范","成都体育学院","成都信息工程学院","乐山师范","绵阳师范","内江师范"]
		db = tool().get_all_find(query_db("user_db"))
		for x in db:

			school_name =  x.get("school")
			try:
				school_code = school_list.index(school_name)
			except:
				school_code = 0
			x.set("public_type",school_code)
			x.save()
			print "改动成功!目前public_type为:",x.get("public_type")
		return True
	def update_school_type(slef):
		"用来定时更新学校代码,防止出错"
		user_db = tool().get_all_find(query_db("user_db").include("school_id"))
		for x in user_db:
			school_id = x.get("school_id").get("school_id")
			x.set("public_type",int(school_id))
			x.save()
		print "所有用户的学校id更新完成"

	def public_magazine(self,publish):
		try:
			mz = query_db("magazine").equal_to("magazine",publish).equal_to("publish_state",0).ascending("title").first()
			mz.set("publish_state",1)
			mz.save()
		except Exception,e:
			print e




# class file_care:
# 	def upload_file(self,file_):

class tool:
	def get_all_find(self,search_body):
		count = search_body.count()
		re = []
		if count>100:
			loop = (count/100)+1
			for x in range(loop):

				search_list = search_body.skip(x*100).find()
				re += search_list
			return re

		else:
			return search_body.find()

		

	def w_file(self,content):
		with codecs.open("templates/page.html","w","utf-8") as f:
			f.write(content.decode("utf-8"))
		return True

	def creat_page(self):

		male = get_person(2)
		female = get_person(1)
		content = male+female
		w_file(content)
		return "success"

	def get_title(slef,publish_type):
		title = query_db("magazine").equal_to("magazine",int(publish_type)).descending("title").first().get("title")+1
		return title


class method:
	def make_magazine(self,list_str,publish_type):
		"生成杂志正文"
		title=tool().get_title(publish_type)
		user_list = list_str.split("-")
		user_list = [query_db("user_db").get(x) for x in user_list]
		#user_list为queryObject的list
		for x in user_list:
			if x.get("stat")==1:
				return False
		# 如果有状态为1的人(已上架过的)立刻return
		# 获取杂志封面
		cover_obj = query_db("cover_img").equal_to("stat",0).first()
		cover_obj.set("stat",1)
		cover_obj.save()
		"在数据库中生成一期记录"

		mz = init_db("magazine")
		mz.set("user_list",list_str)
		mz.set("title",title)
		mz.set("magazine",int(publish_type))
		mz.set("cover_img",cover_obj)
		mz.set("publish_state",0)
		mz.save()

		title = mz.get("title")

		print "成功建立第"+str(title)+"期杂志"
		for x in user_list:
			objid = x.id
			write_leancloud().change("user_db",objid,{"stat":1,"magazine":mz})
			mail_().send_mail("success",{"contact_email":x.get("contact_email"),"nick_name":x.get("nick_name")})


		#把已选的照片删除掉
		return json.dumps({"stat":200,"data":{"title":title}})
		







		











