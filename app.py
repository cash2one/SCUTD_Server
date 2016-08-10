#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeperfect
# @Date:   2015-09-03 23:23:24
# @Last Modified by:   leeperfect
# @Last Modified time: 2016-03-06 00:04:14
#coding=utf-8
from flask import Flask,request,render_template,session,redirect,url_for
from werkzeug import secure_filename
import os
from leancloud_path import read_leancloud,write_leancloud,tool,method
import time,json
from datetime import timedelta
from tools import mail_
# from wechat_path import write_wechat
from method_ import user_tools,magazine_tools


rl = read_leancloud()
wl = write_leancloud()
tl = tool()
mt = method()
# ww = write_wechat()



import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

sess = session

app.permanent_session_lifetime = timedelta(minutes=20)
SESSION_TYPE = 'filesystem'


def check_login():
	try:
		user_name = sess["user_name"]
		user_pass = sess["user_pass"]
		user_objid = sess["user_objid"]
		return_dic = rl.get_admin(user_name,user_pass)
		if return_dic:
			return return_dic
	except:
		
		return False
# router路由

@app.route("/",methods=["GET","POST"])
def dashboard():
	if not check_login():
		return render_template("login.html")

	try:
		page = int(request.args["page"])-1
	except:
		page = 0
	try:
		publish_type = request.args["publish"]
	except:
		publish_type = 1

	sess["page"] = page
	sess["publish_type"] = publish_type
	
	user_info = rl.get_user_info(page,publish_type)
	

	return render_template("dashboard.html",user_info=user_info)


@app.route("/login",methods=["GET","POST"])
def login():
	if request.method=="POST":
		user_name = request.form["username"]
		user_pass = request.form["password"]
		return_dic = rl.get_admin(user_name,user_pass)
		
	#这里通过参数的方式获得了user_name和user_pass,并且通过这两者获得用户的user_objid

		if return_dic:
			user_objid = return_dic

			sess["user_name"] = user_name
			sess["user_objid"] = user_objid
			sess['user_pass'] = user_pass
			sess["page"] = 1
			sess["publish_type"] = 1

			return redirect(url_for("dashboard"))
		else:
			return "您的管理员账号已注销或账号密码错误"

	else:
		return render_template("login.html")

@app.route("/page",methods=["GET","POST"])
def page():
	if not check_login():
		return render_template("login.html")
	page = request.args["page"]
	magazine = rl.get_magazine(page,sess["publish_type"])
	return render_template("page.html",magazine=magazine,page=page,publish_type=str(sess["publish_type"]))

@app.route("/down",methods=["GET","POST"])
def down():
	# if not check_login():
	# 	return render_template("login.html")
	return render_template("down_user.html")


@app.route("/base",methods=["GET","POST"])
def base():
	return render_template("base.html")
@app.route("/content",methods=["GET","POST"])
def content():
	return render_template("content.html")
@app.route("/head",methods=["GET","POST"])
def head():
	return render_template("head.html")
	
#TODO ajax判断未登录的错误
	

# ======================功能性AJAX路由=======================
@app.route("/get_user_unpost",methods=["GET","POST"])
def get_user_unpost():
	if not check_login():
		return 

	
	page =int(request.args["page"])-1 if "page" in request.args else 0
	publish_type = request.args["publish"] if "publish" in request.args else 1
	
	user_info = rl.get_user_info(page,publish_type)
	user_info = json.dumps(user_info)

	return user_info


@app.route("/make_magazing",methods=["GET","POST"])
def make_magazing():
	if not check_login():
		return 
	"传入的user_list为objectId-objectId"
	user_str = request.args["user"]
	re = mt.make_magazine(user_str,sess["publish_type"])
	# ww.new_post(sess["publish_type"])
	if re:
		return re
	else:
		return "2"

	

@app.route("/del_img_by_objid",methods=["GET","POST"])
def del_img_by_objid():
	if not check_login():
		return 
	objid = request.args["del"]
	user_info = rl.get_object("user_db",objid)

	if wl.del_user_by_objid(objid):
		mail_().send_mail("fail",user_info)

		return "1"
	else:
		return "2"

@app.route("/check",methods=["GET","POST"])
def check():
	
	return render_template("check.html")

@app.route("/checkme",methods=["GET","POST"])
def checkme():
	wechat = request.args.get("mail")
	re = rl.find_lc_one("user_db",{"contact_normal":wechat})
	return re

@app.route("/down_people_by_title",methods=["GET","POST"])
def down_people_by_title():
	# if not check_login():
	# 	re_ = {"success":"failed"}
	# 	return re_
	title = request.args["title"]
	magazine = request.args["magazine"]
	index_ = request.args["index_"]
	print "beee"
	re_ = user_tools().down_user_by_title(title,magazine,index_)
	print re_
	return re_

@app.route("/down_people_unpublished",methods=["GET","POST"])
def down_people_():
	# if not check_login():
	# 	re_ = {"success":"failed"}
	# 	return re_
	wechat_id = request.args["wechat_id"]
	re_ = user_tools().down_user_unpublished(wechat_id)
	return re_
	
@app.route("/get_title_list",methods=["GET","POST"])
def get_title_list():
	magazine = request.args["magazine"]
	re_ = rl.get_title_list(magazine)
	re_ = json.dumps(re_)
	return re_
@app.route("/update_school_id",methods=["GET","POST"])
def update_school_id():
	print "吼啊"
	wl.update_school_type()
	print "当然啦"
	return {"success":"success"}
	

	

		
	



	

	

		
		
		



	
	




# if __name__ == "__main__":
# 	app.run(debug=True)
