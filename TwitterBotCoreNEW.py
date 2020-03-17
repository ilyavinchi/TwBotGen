# -*- coding: utf-8 -*-
import time
import os
import sys
import json
import random as r
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import clipboard
import uuid
import threading
from threading import Thread
import pickle
import requests
from PIL import Image
import telebot
from shutil import rmtree

accounts = os.listdir("Accounts/")

# dic = {}
# for x in range(len(accounts)):
# 	dic.update({accounts[x]: '-'})
# pickle.dump(dic, open("Accounts_timers/posting_timers.pkl", "wb"))
# pickle.dump(dic, open("Accounts_timers/subscribe_timers.pkl", "wb"))

# print(pickle.load(open("Accounts_timers/posting_timers.pkl", "rb")))
# print(pickle.load(open("Accounts_timers/subscribe_timers.pkl", "rb")))

# print(pickle.load(open("Accounts/Janice Griffith/settings/enter.pkl", "rb")))

with open('Accounts_timers/posting_timers.pkl', 'rb') as m:
	p_l = pickle.load(m)
p_l['Kaylee Jewel'] = "-"
with open('Accounts_timers/posting_timers.pkl', 'wb') as m:
	pickle.dump(p_l, m)

with open('Accounts_timers/subscribe_timers.pkl', 'rb') as f:
	s_l = pickle.load(f)
s_l['Kaylee Jewel'] = "-"
with open('Accounts_timers/subscribe_timers.pkl', 'wb') as f:
	pickle.dump(s_l, f)

print(pickle.load(open("Accounts_timers/posting_timers.pkl", "rb")))
print(pickle.load(open("Accounts_timers/subscribe_timers.pkl", "rb")))

autosubscribe_threads = 0
autoposting_threads = 0
account_gen_active = False
works = True

def logging(logging_name, logging_data):
	if os.path.exists('Accounts_logs/' + logging_name + ".log"):
		with open('Accounts_logs/' + logging_name + ".log", 'a') as f:
			f.write(logging_data)
	else:
		with open('Accounts_logs/' + logging_name + ".log", 'w') as f:
			f.write(logging_data)		

def wait(dr, el_info, tries, wait_type):
	# 1 - url
	if wait_type == 2:
		for x in range(tries*10):
			try:
				elem = dr.find_element(By.XPATH, el_info)
				return elem
			except:
				time.sleep(0.1)	
	elif wait_type == 3:
		for x in range(tries*30):
			try:
				elem = dr.find_elements(By.XPATH, el_info)
				return elem
			except:
				time.sleep(0.1)	

	print("ERROR ", el_info)
	elem = dr.find_elements(By.XPATH, el_info)
	return False

def phone_gen():
	phone_numb_search = requests.get('http://api.sms-reg.com/getNum.php?country=ru&service=twitter&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	phone_numb_search = phone_numb_search.text
	json_phone_numb_search = json.loads(phone_numb_search)
	response_phone_numb_search = json_phone_numb_search['response']
	phone_search_tzid = json_phone_numb_search['tzid']
	while True:
		phone_numb_info = requests.get('http://api.sms-reg.com/getState.php?tzid=' + phone_search_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		phone_numb_info = phone_numb_info.text
		json_phone_numb_info = json.loads(phone_numb_info)
		if json_phone_numb_info['response'] == 'WARNING_NO_NUMS':
			return False, False
		elif json_phone_numb_info['response'] == 'TZ_INPOOL':
			time.sleep(2)
		elif json_phone_numb_info['response'] == 'TZ_NUM_PREPARE':
			return "+" + json_phone_numb_info['number'], phone_search_tzid

def sms_get(p_tzid):
	sms_ready = requests.get('http://api.sms-reg.com/setReady.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	for x in range(650):
		sms_info = requests.get('http://api.sms-reg.com/getState.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		sms_info = sms_info.text
		json_sms_info = json.loads(sms_info)
		if json_sms_info['response'] == 'TZ_NUM_ANSWER':
			return json_sms_info['msg']
		elif json_sms_info['response'] == "TZ_OVER_EMPTY" or json_sms_info['response'] == "TZ_DELETED":
			return 0
		else:
				time.sleep(1)

	return 0

def account_gen():
	print("GEN NEW ACCOUNT")
	options = Options()
	headless = True
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_argument('-–incognito')
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-extensions")
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window()	

	driver.get("https://www.coedcherry.com/models/random")
	pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)
	while len(pictures) < 6:
		driver.get("https://www.coedcherry.com/models/random")
		pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)

	model_name = driver.find_element(By.XPATH, "//h1").text
	model_name = model_name.split(' ')[0] + " " + model_name.split(' ')[1]
	os.mkdir("Accounts/" + model_name)
	os.mkdir("Accounts/" + model_name + "/imgs")
	pictures_href = []
	for x in range(6):
		pictures_href.append(pictures[x].get_attribute("href"))

	for x in range(6):
		driver.get(pictures_href[x])
		pictures_second = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)
		
		for z in range(len(pictures_second)):
			with open("Accounts/" + model_name + "/imgs/" + str(uuid.uuid1()).replace("-", "")[:10] + ".jpg", 'wb') as file:
				file.write(requests.get(pictures_second[z].get_attribute("href")).content)


	phone, phone_tzid = phone_gen()
	if phone:
		driver.get("https://twitter.com/i/flow/signup")
		wait(driver, "//input[@type='text']", 10, 2).send_keys(model_name)
		wait(driver, "//input[@type='tel']", 10, 2).send_keys(phone)
		while True:
			if wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 2):
				wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 2).click()
				break
			else:
				wait(driver, "//div/span/span", 1, 2).click()

		code = sms_get(phone_tzid)
		if code == 0:
			rmtree("Accounts/" + model_name)
			return False
		wait(driver, "//input[@name='verfication_code']", 10, 2).send_keys(code)
		wait(driver, "//div/div/div/div[@role='button']/div/span/span", 10, 2).click()
		acc_password = "WWW2714070" + list(model_name)[0]
		wait(driver, "//input[@name='password']", 10, 2).send_keys(acc_password)
		while True:
			try:
				wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 2).click()
				time.sleep(1)
				continue
			except:
				break
				
		driver.get("https://twitter.com/home")

		requests.get('http://api.sms-reg.com/setOperationOk.php?tzid=' + phone_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		os.mkdir("Accounts/" + model_name + "/cookies")
		pickle.dump( driver.get_cookies() , open("Accounts/" + model_name + "/cookies/cookies.pkl","wb"))

		os.mkdir("Accounts/" + model_name + "/databases")
		os.mkdir("Accounts/" + model_name + "/settings")
		os.mkdir("Accounts/" + model_name + "/statistic")
		a_statistic = ["OFF",0, 0]
		pickle.dump( a_statistic , open("Accounts/" + model_name + "/statistic/" + "autosubscribe.pkl","wb"))
		p_statistic = ["OFF",0, 0, "-"]
		pickle.dump( p_statistic , open("Accounts/" + model_name + "/statistic/" + "autoposting.pkl","wb"))	

		os.system("cls")
		split_name = model_name.split(" ")
		driver.get("https://twitter.com/settings/screen_name")
		try_combinations = [split_name[0] + split_name[1], split_name[1] + split_name[0], split_name[1] +"_"+ split_name[0], split_name[0] +"_"+ split_name[1], split_name[1] + split_name[0] + "_", split_name[0] + split_name[1] + "_", split_name[0] + "_" + split_name[1] + "_", split_name[1] + "_" + split_name[0] + "_"]
		last_login = ''
		login = ''
		for x in range(8):
			if last_login == login:
				last_login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
				while wait(driver, "//input", 10, 2).get_attribute("value") != "":
					wait(driver, "//input", 10, 2).send_keys(Keys.BACK_SPACE)

				wait(driver, "//input", 10, 2).send_keys(try_combinations[x])
				wait(driver, "//div[@data-testid='settingsDetailSave']", 10, 2).click()
				driver.refresh()
				time.sleep(10)
				login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
			else:
				break
		time.sleep(1)
		login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
		driver.get("https://twitter.com/settings/language")
		wait(driver, "//option[@value='en']", 10, 2).click()
		wait(driver, "//div/div/div/span/span", 10, 2).click()
		driver.refresh()
		driver.get("https://twitter.com/settings/country")
		wait(driver, "//option[@value='us']", 10, 2).click()
		wait(driver, "//div[@aria-haspopup='false'][1]", 10, 2).click()
		driver.get("https://twitter.com/" + login)

		driver.get("https://twitter.com/settings/profile")
		list_of_images = os.listdir("Accounts/" + model_name + "/imgs/")
		im = ''
		for x in range(len(list_of_images)):
			im = Image.open("Accounts/" + model_name + "/imgs/" + list_of_images[x])
			w, h = im.size
			if w > h:
				im = list_of_images[x]
				break

			im = list_of_images[r.randint(0, len(list_of_images) - 1)]

		wait(driver, "//div[1]/div[1]/div/div/div/input[@type='file']", 10, 2).send_keys(os.path.abspath("Accounts/" + model_name + "/imgs/" + im))
		wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()
		random_number_for_image = r.randint(0, len(list_of_images) - 1)
		wait(driver, "//div[1]/div[2]/div/div/div/input[@type='file']", 10, 2).send_keys(os.path.abspath("Accounts/" + model_name + "/imgs/" + list_of_images[random_number_for_image]))
		wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()
		url = url_shortener_main(model_name)
		wait(driver, "//textarea[@name='description']", 10, 2).send_keys("Register and find me here - " + url)
		wait(driver, "//input[@name='url']", 10, 2).send_keys(url)
		wait(driver, "//div[1]/div/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()

		pin_post(model_name, login)

		pickle.dump( [login, acc_password, phone_tzid] , open("Accounts/" + model_name + "/settings/enter.pkl","wb"))
		balance_info = requests.get('http://api.sms-reg.com/getBalance.php?apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		balance_info = balance_info.text
		json_balance_info = json.loads(balance_info)
		bot = telebot.TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
		bot.send_message(457184560, "Ваш балланс: " + json_balance_info['balance'])
		print(login, acc_password, phone_tzid)
		print("GEN END")
		return model_name
	else:
		rmtree("Accounts/" + model_name)
		return False

def initialize_settings(bot_name):
	with open("Accounts/" + bot_name + "/settings/_settings.json") as f:
		settings = json.load(f)
	return settings

def cookie_creator(bot_name):
	options = Options()
	headless = False
	options.headless = headless
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window()	
	driver.get("https://twitter.com/home")
	time.sleep(6)
	while driver.current_url != "https://twitter.com/home":
		time.sleep(1)
	pickle.dump( driver.get_cookies() , open("Accounts/" + bot_name + "/cookies/cookies.pkl","wb"))
	driver.quit()

def driver_start(bot_name, dr_headless):
	options = Options()
	headless = dr_headless
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_argument('-–incognito')
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-extensions")
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window()	
	driver.get("https://twitter.com/home")
	for cookie in pickle.load(open("Accounts/" + bot_name + "/cookies/cookies.pkl", "rb")):
		if 'expiry' in cookie:
			del cookie['expiry']
			driver.add_cookie(cookie)
	driver.refresh()
	return driver

def parsing_first_type(dr, send_parsing_text, p_l):
	driver = dr
	driver.get("https://twitter.com/search")
	el = wait(driver, "//input[@data-testid='SearchBox_Search_Input']", 10, 2)
	el.click()
	el.send_keys(send_parsing_text)
	time.sleep(2)
	wait(driver, "//div[@id='typeaheadDropdown-1']/div[2]", 10, 2).click()
	time.sleep(2)
	driver.get(wait(driver, "//div[@role='tablist']/div[2]/a", 10, 2).get_attribute("href"))
	driver.refresh()
	time.sleep(2)
	logins = wait(driver, "//div[@dir='ltr']/span", 10, 3)
	ready_logins = []
	for i in range(p_l):
		ready_logins.append(logins[i].text.replace("@", ""))
	return ready_logins



def autosubscribe_start(s1, s2, s3, s4, s5, s6, s7):
	global autosubscribe_threads
	global works
	s_s = [s1, s2, s3, s4, s5, s6, s7]
	driver = driver_start(s_s[0], s_s[5])
	subscribe_base = []
	if os.path.exists("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl"):
		subscribe_base = pickle.load(open("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl", "rb"))
	else:
		subscribe_base = []

	enter = []
	enter = pickle.load(open("Accounts/" + s_s[0] + "/settings/enter.pkl", "rb"))
	driver.get("https://twitter.com/" + enter[0])
	try:
		following_count = int(wait(driver, "//a[@href='/" + enter[0] + "/following']", 30, 2).text.split(" ")[0])
	except:
		following_count = 0

	if following_count < 4700:
		count_of_realsubscribe = 0
		while (count_of_realsubscribe != s_s[1]):
			if works:
				if(len(subscribe_base) == 0):
					p_accept = True
					while p_accept:
						try:
							subscribe_base = parsing_first_type(driver, s_s[4], s_s[6])
							p_accept = False
						except:
							continue
					
					pickle.dump( subscribe_base , open("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl","wb"))
					interval_between_subscribe = r.randint(s_s[2], s_s[3])
					if count_of_realsubscribe != 0:
						time.sleep(interval_between_subscribe)
				try:
					driver.get("https://twitter.com/" + subscribe_base[0])
					wait(driver, "//div[@data-testid='placementTracking']/div/div/div[1]", 10, 2).click()
					time.sleep(2)
					if wait(driver, "//div[@data-testid='placementTracking']/div/div/div[1]", 10, 2).text == "Follow":
						autosubscribe_statistic = ["GET BANNED",count_of_realsubscribe, s_s[1]]
						pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))
						break
					count_of_realsubscribe += 1
					subscribe_base.pop(0)
					pickle.dump( subscribe_base , open("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl","wb"))

					if (count_of_realsubscribe != s_s[1] and len(subscribe_base) != 0):
						interval_between_subscribe = r.randint(s_s[2], s_s[3])
						autosubscribe_statistic = ["WORKING",count_of_realsubscribe, s_s[1]]
						pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))
						time.sleep(interval_between_subscribe)
					else:
						if count_of_realsubscribe != s_s[1]:
							autosubscribe_statistic = ["Parsing",count_of_realsubscribe, s_s[1]]
							pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))
						else:
							autosubscribe_statistic = ["END WORK",count_of_realsubscribe, s_s[1]]
							pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))

				except:
					time.sleep(3)
					if driver.current_url == "https://twitter.com/account/access":	
						if access(driver, s_s[0]):
							continue
						else:
							autosubscribe_threads -= 1
							rmtree('Accounts/' + s_s[0])
							p_l = {}
							s_l = {}

							while True:
								try:
									with open('Accounts_timers/posting_timers.pkl', 'rb') as f:
										p_l = pickle.load(f)
									with open('Accounts_timers/subscribe_timers.pkl', 'rb') as f:
										s_l = pickle.load(f)
									p_l.pop(s_s[0])
									s_l.pop(s_s[0])

									with open('Accounts_timers/posting_timers.pkl', 'wb') as f:
										pickle.dump(p_l, f)
									with open('Accounts_timers/subscribe_timers.pkl', 'wb') as f:
										pickle.dump(s_l, f)
									break
								except:
									time.sleep(1)
							return False
							break
							# 'Accounts_timers/subscribe_timers.pkl'
					else:
						autosubscribe_statistic = ["ERROR",count_of_realsubscribe, s_s[1]]
						pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))
						subscribe_base.pop(0)
						continue
			else:
				break
	else:
			count_of_desubscribe = 0 
			driver.get("https://twitter.com/" + enter[0] +"/following")
			followings = wait(driver, "//div[@aria-label='Timeline: Following']/div/div/div/div/div/div/div/div/div/div", 10, 3)
			while len(followings) < 300:
				wait(driver, "//div[@aria-label='Timeline: Following']", 10, 2).sendKeys(Keys.PAGE_DOWN);
				followings = wait(driver, "//div[@aria-label='Timeline: Following']/div/div/div/div/div/div/div/div/div/div", 10, 3)
			while (count_of_desubscribe < 301):
				if works:
					try:
						driver.get("https://twitter.com/" + followings[0])
						wait(driver, "//div[@data-testid='placementTracking']/div/div/div[1]", 10, 2).click()
						wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 10, 2).click()
						followings.pop(0)
						count_of_desubscribe += 1
					except:
						followings.pop(0)
						count_of_desubscribe += 1
				else:
					break
	
	autosubscribe_threads -= 1
	while True:
		try:
			s_l = {}
			with open('Accounts_timers/subscribe_timers.pkl', 'rb') as f:
				s_l = pickle.load(f)
			s_l[s_s[0]] = time.time() + 86400
			with open('Accounts_timers/subscribe_timers.pkl', 'wb') as f:
				pickle.dump(s_l, f)	
			break
			return True
		except:
				time.sleep(1)

def url_shortener_sec(bot_name):
	options = Options()
	headless = True
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_argument('-–incognito')
	options.add_argument("--disable-notifications")
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window()	
	driver.get("https://is.gd/create.php")
	# link_to_shorter = initialize_settings(bot_name)['offer_link']
	link_to_shorter = 'slmshop.tk'
	driver.find_element(By.XPATH, "//input[@class='urlbox']").send_keys(link_to_shorter)
	driver.find_element(By.XPATH , "//div[@id='shorturllabel']/label").click()

	bot_name = bot_name.split(" ")
	if len(bot_name) == 1:
		bot_name = bot_name[0]
	else:
		bot_name = bot_name[0] + bot_name[1]

	if bot_name[-1:] != "_":
		link_save = bot_name + '_' + str(uuid.uuid1()).replace("-", "")[:6]
	else:
		link_save = bot_name + str(uuid.uuid1()).replace("-", "")[:6]
	driver.find_element(By.XPATH , "//input[@class='shorturlbox']").send_keys(link_save)
	driver.find_element(By.XPATH, "//input[@id='logstats']").send_keys(Keys.SPACE)
	driver.find_element(By.XPATH , "//input[@class='submitbutton']").submit()
	wait(driver, "//input[@id='short_url']", 10, 2)
	# while wait(driver, "//input[@id='short_url']", 10, 2).text != ("https://is.gd/" + link_save):
	# 	time.sleep(0.1)
	driver.quit()
	return " https://is.gd/" + link_save

def url_shortener_main(bot_name):
	options = Options()
	headless = True
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_argument('-–incognito')
	options.add_argument("--disable-notifications")
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window()	
	driver.get("https://is.gd/create.php")
	# link_to_shorter = initialize_settings(bot_name)['offer_link']
	link_to_shorter = 'slmshop.tk'
	driver.find_element(By.XPATH, "//input[@class='urlbox']").send_keys(link_to_shorter)
	driver.find_element(By.XPATH , "//div[@id='shorturllabel']/label").click()

	bot_name = bot_name.split(" ")
	if len(bot_name) == 1:
		bot_name = bot_name[0]
	else:
		bot_name = bot_name[0] + bot_name[1]

	link_save = bot_name
	driver.find_element(By.XPATH , "//input[@class='shorturlbox']").send_keys(link_save)
	driver.find_element(By.XPATH, "//input[@id='logstats']").send_keys(Keys.SPACE)
	driver.find_element(By.XPATH , "//input[@class='submitbutton']").submit()
	wait(driver, "//input[@id='short_url']", 10, 2)
	# while wait(driver, "//input[@id='short_url']", 10, 2).text != ("https://is.gd/" + link_save):
	# 	time.sleep(0.1)
	driver.quit()
	return "https://is.gd/" + link_save

def autoposting_start(a1, a2, a3):
	global works
	global autoposting_threads
	a_s = [a1, a2, a3]
	list_of_images = os.listdir("Accounts/" + a_s[0] + "/imgs/")
	count_of_posts = 0
	while count_of_posts < a_s[1]:
		if works:
			try:
				if(list_of_images != 0):
					driver = driver_start(a_s[0], False)
					random_number_for_image = r.randint(0, len(list_of_images) - 1)
					all_texts = open("Accounts_lists/texts.txt", 'r', encoding="utf-8").read().split("\n\n")
					contents_from_file = all_texts[r.randint(0, len(all_texts) - 1)] + url_shortener_sec(a_s[0])
					clipboard.copy(contents_from_file)
					el = wait(driver, "//div[@class='notranslate public-DraftEditor-content']", 10, 2)
					el.click()
					el.send_keys(Keys.CONTROL, 'v')
					time.sleep(2)
					wait(driver, "//input[@type='file']", 10, 2).send_keys(os.path.abspath("Accounts/" + a_s[0] + "/imgs/" + list_of_images[random_number_for_image]))
					time.sleep(5)
					wait(driver, "//div[@data-testid='tweetButtonInline']", 10, 2).send_keys(Keys.ENTER)
					time.sleep(2)
					count_of_posts += 1
					driver.quit()

					if count_of_posts < a_s[1]:
						time_next_post = time.ctime(time.time() + a_s[2]).split(" ")[3]
						autoposting_statistic = ["WORKING",count_of_posts, a_s[1], time_next_post]
						pickle.dump( autoposting_statistic , open("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl","wb"))
						time.sleep(a_s[2])
					else:
						autoposting_statistic = ["END WORK",count_of_posts, a_s[1], "--:--:--"]
						pickle.dump( autoposting_statistic , open("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl","wb"))
			except:
				autoposting_threads -= 1
				break
				return False
		else:
			break
	autoposting_threads -= 1
	while True:
		try:
			p_l = {}
			with open('Accounts_timers/posting_timers.pkl', 'rb') as f:
				p_l = pickle.load(f)
			p_l[a_s[0]] = time.time() + 86400
			with open('Accounts_timers/posting_timers.pkl', 'wb') as f:
				pickle.dump(p_l, f)

			break
			return True
		except:
			time.sleep(1)

def pin_post(pin_bot_name, pin_login):
	autoposting_start(pin_bot_name, 1, 0)
	driver = driver_start(pin_bot_name, False)
	driver.get("https://twitter.com/" + pin_login)
	wait(driver, "//div[@data-testid='caret']", 10, 2).click()
	wait(driver, "//div[@data-testid='pin']", 10, 2).click()
	wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 10, 2).click()	

def accounts_activator(path_timers):
	global account_gen_active
	if account_gen_active:
		return False
	else:
		while True:
			try:
				with open(path_timers, 'rb') as f:
					l = pickle.load(f)
				break
			except:
				time.sleep(2)
				continue

		min_name = False
		min_time = 999999999999999
		
		for x in l:
			if l[x] == "+":
				continue
			elif l[x] == "-":
				l[x] = "+"
				with open(path_timers, 'wb') as f:
					pickle.dump(l, f)
				print(x)
				return x
			elif l[x] < min_time:
				min_name = x
				min_time = l[x]

		if min_time > time.time():
			min_name = False

		if min_name:
			return min_name
		else:
			account_gen_active = True
			min_name = account_gen()
			account_gen_active = False
			if min_name:
				while True:
					try:
						p_l = {}
						with open('Accounts_timers/posting_timers.pkl', 'rb') as m:
							p_l = pickle.load(m)
						p_l.update({min_name: "-"})
						with open('Accounts_timers/posting_timers.pkl', 'wb') as m:
							pickle.dump(p_l, m)
						break
					except:
						time.sleep(1)
				while True:
					try:
						s_l = {}
						with open('Accounts_timers/subscribe_timers.pkl', 'rb') as f:
							s_l = pickle.load(f)
						s_l.update({min_name: "-"})
						with open('Accounts_timers/subscribe_timers.pkl', 'wb') as f:
							pickle.dump(s_l, f)
						break
					except:
						time.sleep(1)

				print(pickle.load(open("Accounts_timers/posting_timers.pkl", "rb")))
				print(pickle.load(open("Accounts_timers/subscribe_timers.pkl", "rb")))

			return False

def autosubscribe_add(a_t):
	global autosubscribe_threads
	global works
	default_max_autosubscribe_bots = 2
	default_massfolowing = ""
	default_gui = ''
	default_limit_subscribes = 250
	default_interval = "60-90"
	default_parsing_limit = 5
	default_parsing_type = 3
	default_words = "nude sex tits"
	default_lang = 1
	while works:
		while autosubscribe_threads < default_max_autosubscribe_bots:
			print("AUTOSUBSCRIBE_ADD")
			account = accounts_activator("Accounts_timers/subscribe_timers.pkl")
			if account:
				gui_off = True
				limit_subscribes = default_limit_subscribes
				interval = default_interval
				start_interval = int(interval.split("-")[0])
				end_interval = int(interval.split("-")[1])
				parsing_limit = default_parsing_limit
				parsing_type = default_parsing_type
				if os.path.exists("Accounts/" + account + "/databases/subscribe_base.pkl"):
					os.remove("Accounts/" + account + "/databases/subscribe_base.pkl")	
				words = default_words
				words = words.split(" ")
				ready_string = "("
				for l in range(len(words)):
					if l != len(words)-1:
						ready_string = ready_string + words[l] + " OR "
					else:
						ready_string = ready_string + words[l]
				ready_string += ")"
				send_text = (ready_string)

				autosubscribe_statistic = ["STARTING",0, limit_subscribes]
				pickle.dump( autosubscribe_statistic , open("Accounts/" + account + "/statistic/" + "autosubscribe.pkl","wb"))
				Thread(target=autosubscribe_start, args=(account, limit_subscribes, start_interval, end_interval, send_text, gui_off, parsing_limit)).start()
				autosubscribe_threads += 1
				print(autosubscribe_threads)
			time.sleep(10)

def autoposting_add(v_p):
	global autoposting_threads
	global works
	default_max_autoposting_bots = 2
	default_autoposting = ""
	default_limit_posts = 5
	default_interval_between_posts = 2
	while works:
		while autoposting_threads < default_max_autoposting_bots:
			print("AUTOPOSTING_ADD")
			account = accounts_activator("Accounts_timers/posting_timers.pkl")
			if account:
				limit_posts = default_limit_posts
				interval_between_posts = default_interval_between_posts * 3600
				autoposting_statistic = ["STARTING",0, limit_posts, "NOW"]
				pickle.dump( autoposting_statistic , open("Accounts/" + account + "/statistic/" + "autoposting.pkl","wb"))	
				Thread(target=autoposting_start, args=(account, limit_posts, interval_between_posts)).start()
				autoposting_threads += 1
				print(autoposting_threads)
			time.sleep(30)

Thread(target=autosubscribe_add, args=("1")).start()
Thread(target=autoposting_add, args=("1")).start()

while True:
	commands = ''
	with open("t.cmds", 'r') as f:
		commands = f.read()
	if commands:
		if commands == '1':
			works = False
			print(autosubscribe_threads)
			print(autoposting_threads)
		elif commands == '2':
			print("autosubscribe_threads: " + str(autosubscribe_threads))
			print("autoposting_threads: " + str(autoposting_threads))
		elif commands == '3':
			os.system("cls")
		elif commands == '4':
			print(pickle.load(open("Accounts_timers/posting_timers.pkl", "rb")))
			print(pickle.load(open("Accounts_timers/subscribe_timers.pkl", "rb")))			
		with open("t.cmds", 'w') as f:
			f.write("")
	time.sleep(5)