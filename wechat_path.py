#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeperfect
# @Date:   2015-10-29 22:38:25
# @Last Modified by:   leeperfect
# @Last Modified time: 2016-01-22 12:46:02
from flask import Flask,request,render_template,session
import os,json
from wechat_sdk_ import WechatExt
import requests
from PIL import Image
from StringIO import StringIO
from leancloud_path import read_leancloud,write_leancloud,tool,method
from bs4 import BeautifulSoup	



rl = read_leancloud()
wl = write_leancloud()
tl = tool()




class write_wechat:
	"""用来进行微信公众平台的操作"""
	def new_post(self,public_type):
		title_num = tl.get_title(public_type)-1

		if int(public_type)==1:
			title = "【川大脱单】第"+str(title_num)+"期"
			wechat = wechat_td
			pic_id = wechat.upload_file('./static/img/cover-scutd.jpg')

		elif int(public_type)==0:
			title = "【脱单大表哥】第"+str(title_num)+"期"
			wechat = wechat_dbg
			pic_id = wechat.upload_file('./static/img/cover-dbg.jpg')
		
		list_ = [{'title': title,'author': '机械李大猫','summary': ' ','content': '请填充内容','picture_id': pic_id,'from_url': 'http://www.sojump.com/jq/4949027.aspx'}]
		wechat.add_news(list_)
		return True

	def get_post_list(self):
		news_list = wechat_td.get_news_list(0,10)
		news_to_update = [x["multi_item"][0] for x in news_list]
		for y in news_to_update:
			content_url = y["content_url"]
			sub_title = y["digest"]
			content_html = Beautifulsoup(requests.get(content_url).content)
			news = {
				title :"",
				author : "机械李大猫",
				summary : "",
				content : "",
				picture :"",
				from_url : ""
				}
			




# if __name__=="__main__":
# 	write_wechat().














