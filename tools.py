#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: leeperfect
# @Date:   2015-10-05 19:05:54
# @Last Modified by:   leeperfect
# @Last Modified time: 2016-02-20 14:28:01




import json,time
import codecs
from StringIO import StringIO
import re
# ========= Spider ============
import requests
from requests import Request, Session
from bs4 import BeautifulSoup
# ========= Leancloud ============
import leancloud
from leancloud import Query,Object,User,LeanCloudError,File

#SCU-TD的leancloud配置


# ==================初始化====================
def query_db(db_name):
	db_object = Object.extend(db_name)
	
	db_query = Query(db_object)
	
	return db_query


def init_db(db_name):
	db_object = Object.extend(db_name)
	db = db_object()
	
	return db



def isEmail(email):

	if len(email) > 7:
		if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None:
			return 1
	return 0

# ==================初始化====================
def get_sess():
	s = requests.Session()
	url = "http://www.sojump.com/login.aspx"
	payload = {
	"__VIEWSTATE":"/wEPDwUKLTYwNzk2NTUwMGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgEFJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkUmVtZW1iZXJNZQ==",
	"__EVENTVALIDATION":"/wEdAAYGXI4geJEsptisBei/jFATO6eeGTgad8ksqhDrfRl8wTkBDO5iLfQzicpFe97ObAwXKJ4BaIwAVqp1tKKAEy0u9OTkg+QdHm5OmdKOuPOcGpV4bqusu2zQztdPuWZ1xvo=",
	"ctl00$ContentPlaceHolder1$UserName":"larascu",
	"ctl00$ContentPlaceHolder1$hfUserName":"",
	"ctl00$ContentPlaceHolder1$Password":"233",
	"ctl00$ContentPlaceHolder1$LoginButton":"登+录"
	}
	s.post(url, data=payload)
	return s


sess = get_sess()
# ==================初始化结束====================



class write_sojump:
	def jump_remove(self,user_active,activity_id):
		url_del = "http://www.sojump.com/Handler/AnswerDeleteHandler.ashx?JoinActivityId="+user_active+"&activityid="+activity_id+"&t="+str(int(time.time()))
		if sess.get(url=url_del).content=="ok":
			return "问卷星ID:"+str(user_active)+" remove success"
	
		

class read_sojump:
	def get_jump_list(self,public_type):
		"从问卷星中获取信息并插入到Leancloud中"
		public_type = int(public_type)
		url = "http://www.sojump.com/wjx/activitystat/viewstatsummaryfull.aspx"

		payload = {

		"__EVENTTARGET":"",
		"__EVENTARGUMENT":"",
		"__EVENTVALIDATION":"/wEdAA/dKECfZ8AlbdNYgz9S0Gz5CalSjv2KWoAqVCtrB+JvmPhAE4DWh6DcswFach0ntcGqGc0sOIoxhf1oJkbvpaZZH0CKlZXnU+beI+nZnUvuXgo8ssPJeyvt9y1nieZTN1tBfE5kxitSDXcgqgX/4Falb3sgJH/rUZh/1YC7RtZWFGBT46IsFA4yB31pY6kD+KFSuwLyHZR+lNeuhV9y1m+QVmgOx40berXxrY9qrvqV/GmqZSjC2Cd21l+5i4tJXvXXZakNEfPTR53AMn/mc4/twcUifAfiWk2ZtRGj2LQFkmc/xGKU6Y6F2VQmEHtREFKuT1CrnQ7T8tVNaQxV4Ixh4EFEXg==",
			"__VIEWSTATE":"/wEPDwUKLTI0NjUxOTUyOGRkyOFcEqsq3J0ERN2wvJxsf7urLTU=",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$hfCurPage":"1",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$ddlPageCount":"100",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$hfPageCount":"100",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$btnPC":"修改",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$hfType":"0",
			"ctl02$ContentPlaceHolder1$ViewStatSummary1$hfView":"0"
		}
		pa = {
			"activity":search_attr[public_type-1]
		}
		r = sess.post(url,data=payload,params=pa)
		html = BeautifulSoup(r.content,"html.parser")
		a = html.select("table.result tbody tr")
		if len(a)>0:
			for x in a:

				active_id = x["jid"]
				td = x.select("td")
				
				# 拉取学校列表
				school_sojump = td[12].get_text()
				school_list = query_db("school").find()
				school_ = {}
				for x in school_list:
					school_name = x.get("school_name")
					school_index = x.id
					school_[school_name] = school_index
				try:
					# 如果学校名称在列表中的话,获得学校的pointer
					if school_sojump in school_:
						school_id = query_db("school").get(school_[school_sojump])
					else:
						school_id = query_db("school").get("566c5ea760b25b0437139b05")
				except Exception,e:
					print e
					print active_id," school"


				
				photo_ = td[15].select("a")[0]["href"]
				file_photo = File('avatar.jpg', StringIO(requests.get(photo_).content),'jpg').save()
				photo_list = [file_photo.id]



				card_photo = td[16].select("a")[0]["href"]

				if StringIO(requests.get(card_photo).content)==StringIO(requests.get(photo_).content):
					print "又有一个重复提交照片的SB"
					card_photo_list = [file_photo.id]
				else:
					file_card = File('card.jpg', StringIO(requests.get(card_photo).content),'jpg').save()
					card_photo_list = [file_card.id]

				photo = query_db("_File").get(file_photo.id)
 				card_photo = query_db("_File").get(file_card.id)

				user_info = {
							"stat":0,
							"active_id":active_id,
							"time_creat":td[2].get_text(),
							"time_spend":td[3].get_text(),
							"ip_address":td[4].get_text(),
							"from":td[5].get_text(),
							"from_detailed":td[6].get_text(),
							"nick_name":td[7].get_text(),
							"sex":td[8].get_text(),
							"age":td[9].get_text(),
							"height":td[10].get_text(),
							"contact_normal":td[11].get_text(),
							"school":school_sojump,
							"school_id":school_id,
							"hobbies":td[13].get_text(),
							"prefer":td[14].get_text(),
							"photo":photo_list,
							"card_photo":card_photo_list,
							"user_photo":photo,
							"user_card_photo":card_photo,
							"contact_email":td[17].get_text(),
							"hometown":td[18].get_text(),
							"public_type":public_type
				}
				remove = write_sojump().jump_remove(active_id,search_attr[public_type-1])
				#先删除数据
				user_db = init_db("user_db")

				query_user_normal = query_db("user_db").equal_to("contact_normal",user_info["contact_normal"])
				# ====防止重复提交====
				if query_user_normal.count()>0:
					user_info_exist = query_user_normal.first()
					if user_info_exist.get("stat")==3:
						print "已删除用户重新报名"
						user_info_exist.set(user_info)
						user_info_exist.save()
						print "已删除用户妄图重新报名"
					elif user_info_exist.get("stat")==0:
						print "未修改用户更新"
						user_info_exist.set(user_info)
						user_info_exist.save()
						print "未修改用户更新完成"
					elif user_info_exist.get("stat")==1:
						print "上架用户重复报名"
						try:
							mail_().send_mail("exist",user_info)

							print str(user_db)+" created"
						except:
							print "发邮件失败"

					else:
						print "TODO"
				else:
					user_db.set(user_info)
					user_db.save()
					print "提交了新用户,用户名:",user_info["nick_name"]
					# ====防止重复提交====
					try:
						mail_().send_mail("in",user_info)

						print str(user_db)+" created"
					except:
						print "发邮件失败"
				
		return True


class mail_:

	# -*- coding: utf-8 -*-
	def send_mail(self,mail_type,user_info):
		
		send_url = "http://api.sendcloud.net/apiv2/mail/sendtemplate"
		# 输入收件人地址:
		to_addr = user_info["contact_email"]
		
		if mail_type=="in":
			temp = "tuodan_update"
			title = "【川大脱单】报名成功"
		elif mail_type=="success":
			temp = "tuodan_success"
			title = "【川大脱单】审核通过"
		elif mail_type=="fail":
			temp = "tuodan_success"
			title = "【川大脱单】审核通过"
		elif mail_type=="exist":
			temp = "tuodan_re"
			title = "【川大脱单】请勿重复报名"
		para = {"subject":title,
				"from":"lidamao@diangezan.me",
				"templateInvokeName":temp,
				"fromName":"川大脱单-李大猫",
				"xsmtpapi":json.dumps({"to":[to_addr]
					})}

		
		a = requests.post(send_url,data=para)
		if a.status_code==200:
			print "成功向"+user_info["nick_name"].encode('utf-8')+"发送邮件，类型为："+title
		else:
			print "发邮件失败"














