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
import pars

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
		for x in range(tries*10):
			try:
				elem = dr.find_elements(By.XPATH, el_info)
				return elem
			except:
				time.sleep(0.1)	

	print("ERROR ", el_info)
	return False

def phone_gen():
	print("TRY GET NUM")
	phone_numb_search = requests.get('http://api.sms-reg.com/getNum.php?country=ru&service=twitter&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	phone_numb_search = phone_numb_search.text
	print("phone_numb_search: ", phone_numb_search)
	json_phone_numb_search = json.loads(phone_numb_search)
	response_phone_numb_search = json_phone_numb_search['response']
	phone_search_tzid = json_phone_numb_search['tzid']
	print("response_phone_numb_search: ", response_phone_numb_search)
	while True:
		phone_numb_info = requests.get('http://api.sms-reg.com/getState.php?tzid=' + phone_search_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		phone_numb_info = phone_numb_info.text
		json_phone_numb_info = json.loads(phone_numb_info)
		if json_phone_numb_info['response'] == 'WARNING_NO_NUMS':
			print("NO NUMS")
			return False, False
		elif json_phone_numb_info['response'] == 'TZ_INPOOL':
			print("SEARCHING NUMS")
			time.sleep(2)
		elif json_phone_numb_info['response'] == 'TZ_NUM_PREPARE':
			print("GET NUMS")
			return "+" + json_phone_numb_info['number'], phone_search_tzid

def sms_get(p_tzid):
	sms_ready = requests.get('http://api.sms-reg.com/setReady.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	print("SMS READY")
	while True:
		sms_info = requests.get('http://api.sms-reg.com/getState.php?tzid=' + p_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		sms_info = sms_info.text
		print("sms_info: ", sms_info)
		json_sms_info = json.loads(sms_info)
		if json_sms_info['response'] == 'TZ_NUM_ANSWER':
			print("GET ANSWER")
			return json_sms_info['msg'] 
		else:
			print("WAIT FOR ANSWER")
			time.sleep(2)

def account_gen():
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
	driver.get("https://twitter.com/home")
	for cookie in pickle.load(open("Accounts/Amber Hahn/cookies/cookies.pkl", "rb")):
		if 'expiry' in cookie:
			del cookie['expiry']
			driver.add_cookie(cookie)
	driver.refresh()

	print("IMAGES SCRAP START")
	driver.get("https://www.coedcherry.com/models/random")
	pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)
	while len(pictures) < 6:
		driver.get("https://www.coedcherry.com/models/random")
		pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)

	model_name = driver.find_element(By.XPATH, "//h1").text
	model_name = model_name.split(' ')[0] + " " + model_name.split(' ')[1]
	print(model_name)
	os.mkdir("Accounts/" + model_name)
	os.mkdir("Accounts/" + model_name + "/imgs")
	pictures_href = []
	for x in range(6):
		pictures_href.append(pictures[x].get_attribute("href"))

	for x in range(6):
		print(x)
		driver.get(pictures_href[x])
		pictures_second = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 3)
		
		for z in range(len(pictures_second)):
			with open("Accounts/" + model_name + "/imgs/" + str(uuid.uuid1()).replace("-", "")[:10] + ".jpg", 'wb') as file:
				file.write(requests.get(pictures_second[z].get_attribute("href")).content)

	print("IMAGES SCRAP END")

	phone, phone_tzid = phone_gen()
	print("GET PHONE: ", phone_gen)
	print("GET Phone Tzid: ", phone_tzid)
	if phone:
		print("START REGISTRATION")
		driver.get("https://twitter.com/i/flow/signup")
		wait(driver, "//input[@type='text']", 10, 2).send_keys(model_name)
		print("USING NUM")
		wait(driver, "//input[@type='tel']", 10, 2).send_keys(phone)
		while True:
			if wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 2):
				wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 2).click()
				break
			else:
				wait(driver, "//div/span/span", 1, 2).click()

		print("CODE SEARCHING")
		code = sms_get(phone_tzid)
		wait(driver, "//input[@name='verfication_code']", 10, 2).send_keys(code)
		print('1')
		wait(driver, "//div/div/div/div[@role='button']/div/span/span", 10, 2).click()
		print('2')
		acc_password = "WWW2714070" + list(model_name)[0]
		wait(driver, "//input[@name='password']", 10, 2).send_keys(acc_password)
		print('3')
		while wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 2):
			if wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 2):
				wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 2).click()
		driver.get("https://twitter.com/home")

		print("END REGISTRATION")
		requests.get('http://api.sms-reg.com/setOperationOk.php?tzid=' + phone_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		os.mkdir("Accounts/" + model_name + "/cookies")
		pickle.dump( driver.get_cookies() , open("Accounts/" + model_name + "/cookies/cookies.pkl","wb"))

		os.mkdir("Accounts/" + model_name + "/databases")
		os.mkdir("Accounts/" + model_name + "/settings")
		os.mkdir("Accounts/" + model_name + "/statistic")

		os.system("cls")
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=START=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		model_name = "Amber Hahn"
		account_name = model_name
		model_name = model_name.split(" ")
		driver.get("https://twitter.com/settings/screen_name")
		try_combinations = [model_name[0] + model_name[1], model_name[1] + model_name[0], model_name[1] +"_"+ model_name[0], model_name[0] +"_"+ model_name[1], model_name[1] + model_name[0] + "_", model_name[0] + model_name[1] + "_", model_name[0] + "_" + model_name[1] + "_", model_name[1] + "_" + model_name[0] + "_"]
		last_login = ''
		login = ''
		print("CHANGING LOGIN")
		for x in range(8):
			if last_login == login:
				last_login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
				while wait(driver, "//input", 10, 2).get_attribute("value") != "":
					wait(driver, "//input", 10, 2).send_keys(Keys.BACK_SPACE)

				wait(driver, "//input", 10, 2).send_keys(try_combinations[x])
				wait(driver, "//div[@data-testid='settingsDetailSave']", 10, 2).click()
				driver.refresh()
				time.sleep(3)
				login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
			else:
				break
		print("END CHANGING LOGIN")
		time.sleep(1)
		login = wait(driver, "//div[@role='tablist']/div/h2", 10, 2).text
		print("CHANGING LANGUAGE")
		driver.get("https://twitter.com/settings/language")
		wait(driver, "//option[@value='en']", 10, 2).click()
		wait(driver, "//div/div/div/span/span", 10, 2).click()
		driver.refresh()
		driver.refresh()
		print("END CHANGING LANGUAGE")
		print("CHANGING COUNTRY")
		driver.get("https://twitter.com/settings/country")
		wait(driver, "//option[@value='us']", 10, 2).click()
		wait(driver, "//div[@aria-haspopup='false'][1]", 10, 2).click()
		print("END CHANGING COUNTRY")
		driver.get("https://twitter.com/" + login)

		print("EDITING PROFILE")
		driver.get("https://twitter.com/settings/profile")
		list_of_images = os.listdir("Accounts/" + account_name + "/imgs/")
		im = ''
		for x in range(len(list_of_images)):
			im = Image.open("Accounts/" + account_name + "/imgs/" + list_of_images[x])
			w, h = im.size
			if w > h:
				im = list_of_images[x]
				break

			im = list_of_images[r.randint(0, len(list_of_images) - 1)]

		print("LOAD AVATAR")
		wait(driver, "//div[1]/div[1]/div/div/div/input[@type='file']", 10, 2).send_keys(os.path.abspath("Accounts/" + account_name + "/imgs/" + im))
		wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()
		print("END LOAD AVATAR")
		random_number_for_image = r.randint(0, len(list_of_images) - 1)
		print("LOAD HOR")
		wait(driver, "//div[1]/div[2]/div/div/div/input[@type='file']", 10, 2).send_keys(os.path.abspath("Accounts/" + account_name + "/imgs/" + list_of_images[random_number_for_image]))
		wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()
		print("END LOAD HOR")
		url = "https://is.gd/AmberHahn"
		# url = url_shortener_main(account_name)
		print("ARIAS WRITING")
		wait(driver, "//textarea[@name='description']", 10, 2).send_keys("Register and find me here - " + url)
		wait(driver, "//input[@name='url']", 10, 2).send_keys(url)
		print("END ARIAS WRITING")
		wait(driver, "//div[1]/div/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 2).click()
		print("SAVE")
		print("AUTOPOSTING START")
		autoposting_start(account_name, 1, 0, 0)
		print("AUTOPOSTING END")
		print("PIN START")
		driver.get("https://twitter.com/" + login)
		wait(driver, "//div[@data-testid='caret']", 10, 2).click()
		wait(driver, "//div[@data-testid='pin']", 10, 2).click()
		wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 10, 2).click()
		print("PIN END")
		print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=CONGRATULATIONS=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
		driver.save_screenshot("screenshot1.png")
	else:
		print("PHONE NOT FIND")
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

def autosubscribe_start(s1, s2, s3, s4, s5, s6, s7):
	s_s = [s1, s2, s3, s4, s5, s6, s7]
	driver = driver_start(s_s[0], s_s[5])
	subscribe_base = []
	if os.path.exists("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl"):
		subscribe_base = pickle.load(open("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl", "rb"))
	else:
		subscribe_base = []

	count_of_realsubscribe = 0
	while (count_of_realsubscribe != s_s[1]):
		if(len(subscribe_base) == 0):
			subscribe_base = parsing_first_type(driver, s_s[4], s_s[6])
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
			autosubscribe_statistic = ["ERROR",count_of_realsubscribe, s_s[1]]
			pickle.dump( autosubscribe_statistic , open("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl","wb"))
			subscribe_base.pop(0)
			continue

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

def autoposting_start(a1, a2, a3, a4):
	a_s = [a1, a2, a3, a4]
	list_of_images = os.listdir("Accounts/" + a_s[0] + "/imgs/")
	count_of_posts = 0
	time.sleep(a_s[3])
	while count_of_posts < a_s[1]:
		if(list_of_images != 0):
			driver = driver_start(a_s[0], False)
			random_number_for_image = r.randint(0, len(list_of_images) - 1)
			all_texts = open("Accounts_lists/texts.txt", 'r', encoding="utf-8").read().split("\n\n")
			# url = " z5077528.beget.tech/index"+str(r.randint(0, 999))+".html"
			contents_from_file = all_texts[r.randint(0, len(all_texts) - 1)] + url_shortener_sec(a_s[0])
			clipboard.copy(contents_from_file)
			# el = driver.find_element(By.XPATH, "//div[@class='notranslate public-DraftEditor-content']")
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
				time_next_post = time.ctime(time.time() + a_s[2]).split(" ")[4]
				autoposting_statistic = ["WORKING",count_of_posts, a_s[1], time_next_post]
				# pickle.dump( autoposting_statistic , open("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl","wb"))
				time.sleep(a_s[2])
			else:
				autoposting_statistic = ["END WORK",count_of_posts, a_s[1], "--:--:--"]
				# pickle.dump( autoposting_statistic , open("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl","wb"))

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
	wait(driver, wait(driver, "//div[@role='tablist']/div[2]/a", 10, 2).get_attribute("href"), 10, 1)
	driver.refresh()
	time.sleep(2)
	logins = wait(driver, "//div[@dir='ltr']/span", 10, 3)
	ready_logins = []
	for i in range(p_l):
		ready_logins.append(logins[i].text.replace("@", ""))
	return ready_logins



# account_gen()

# # accounts = os.listdir("Accounts/")
# accounts = ['AngelyGrace']
# accounts_statistic = []
# threads = []

# default_massfolowing = ""
# default_gui = ''
# default_limit_subscribes = "300"
# default_interval = "60-90"
# default_parsing_limit = "5"
# default_parsing_type = "3"
# default_words = "nude porn sex"
# default_lang = "1"

# default_autoposting = ""
# default_limit_posts = "5"
# default_interval_between_posts = "2"
# default_time_add = len(accounts)
# default_time_increaser = 3

# for x in range(len(accounts)):
# 	os.system("cls")
# 	print(accounts[x])
# 	settings = initialize_settings(accounts[x])

# 	if os.path.exists("Accounts/" + accounts[x] + "/cookies/cookies.pkl"):
# 		pass
# 	else:
# 		print("~~~~~~~~~~~~~~Войдите в аккаунт~~~~~~~~~~~~~~")
# 		cookie_creator(accounts[x])

# 	massfolowing = input("Запустить массфоловинг? ", ) or default_massfolowing
# 	if massfolowing:
# 		gui = input("Без GUI? ") or default_gui
# 		gui = True if gui else False
# 		limit_subscribes = int(input("На скольких подписаться? ", ) or default_limit_subscribes)
# 		interval = input("Интервал между подписками? (сек) ", ) or default_interval
# 		start_interval = int(interval.split("-")[0])
# 		end_interval = int(interval.split("-")[1])
# 		parsing_limit = int(input("Сколько парсить за раз? ", ) or default_parsing_limit)
# 		print("\nТип парсинга: ")
# 		print("Поиск:")
# 		print("Язык [1] 	", "слово [2] 	","слова [3] 	" )
# 		print("Подписчики групп:" )
# 		print("С одной [4] 	", "С нескольких [5]")
# 		print("С постов:" )
# 		print("С одной [6] 	", "С нескольких [7]")
# 		parsing_type = int(input("Выберите цифру: ", ) or default_parsing_type)
# 		if parsing_type < 4:
# 			if os.path.exists("Accounts/" + accounts[x] + "/databases/subscribe_base.pkl"):
# 				os.remove("Accounts/" + accounts[x] + "/databases/subscribe_base.pkl")
# 			if parsing_type == 1:
# 				lang = int(input("Выберите язык: \nfr[1], en[2], da[3], no[4], de[5]\nВыберите цифру: ") or default_lang)
# 				if lang == 1:
# 					send_text = ("lang:" + "fr")
# 				elif lang == 2:
# 					send_text = ("lang:" + "en")
# 				elif lang == 3:
# 					send_text = ("lang:" + "da")
# 				elif lang == 4:
# 					send_text = ("lang:" + "no")
# 				else:
# 					send_text = ("lang:" + "de")
# 			elif parsing_type == 2:
# 				send_text = (input("Введите слово для поиска: "))
# 			else:
# 				words = input("Введите слова для поиска: ") or default_words
# 				words = words.split(" ")
# 				ready_string = "("
# 				for l in range(len(words)):
# 					if l != len(words)-1:
# 						ready_string = ready_string + words[l] + " OR "
# 					else:
# 						ready_string = ready_string + words[l]
# 				ready_string += ")"
# 				send_text = (ready_string)
# 		elif parsing_type < 6:
# 			print("SECOND")
# 		else:
# 			print("THIRD")

# 		autosubscribe_statistic = ["STARTING",0, limit_subscribes]
# 		pickle.dump( autosubscribe_statistic , open("Accounts/" + accounts[x] + "/statistic/" + "autosubscribe.pkl","wb"))

# 		massfolowing_settings = [accounts[x], limit_subscribes, start_interval, end_interval, send_text, gui, parsing_limit]
# 		threads.append(Thread(target=autosubscribe_start, args=(accounts[x], limit_subscribes, start_interval, end_interval, send_text, gui, parsing_limit)))
# 	else:
# 		autosubscribe_statistic = ["OFF",0, 0]
# 		pickle.dump( autosubscribe_statistic , open("Accounts/" + accounts[x] + "/statistic/" + "autosubscribe.pkl","wb"))

# 	autoposting = input("\nЗапустить автопостинг? ", ) or default_autoposting
# 	if autoposting:
# 		limit_posts = int(input("Сколько постов? ", ) or default_limit_posts)
# 		interval_between_posts = input("Интервал между постами? (часы) ", ) or default_interval_between_posts
# 		interval_between_posts = int(interval_between_posts) * 3600
# 		start_posting = input("Во сколько начать? (h:m) ", ) or time.ctime(time.time()).split(" ")[4].split(":")[0] + ":" + str(int(time.ctime(time.time()).split(" ")[4].split(":")[1])+default_time_add)
# 		hours = int(start_posting.split(":")[0])
# 		minutes = int(start_posting.split(":")[1])
# 		time_now = time.ctime(time.time()).split(" ")[4]
# 		start_seconds = (hours*3600) + (minutes*60)
# 		now_seconds = (int(time_now.split(":")[0])*3600) + (int(time_now.split(":")[1])*60)
# 		if start_seconds >= now_seconds:
# 			start_time = start_seconds - now_seconds
# 		else:
# 			start_time = start_seconds - now_seconds + 86400	

# 		time_next_post = time.ctime(time.time() + start_time).split(" ")[4]
# 		autoposting_statistic = ["STARTING",0, limit_posts, time_next_post]
# 		pickle.dump( autoposting_statistic , open("Accounts/" + accounts[x] + "/statistic/" + "autoposting.pkl","wb"))	

# 		default_time_add += default_time_increaser
# 		autoposting_settings = [accounts[x], limit_posts, interval_between_posts, start_time]
# 		threads.append(Thread(target=autoposting_start, args=(accounts[x], limit_posts, interval_between_posts, start_time)))
# 	else:
# 		autoposting_statistic = ["OFF",0, 0, "--:--:--"]
# 		pickle.dump( autoposting_statistic , open("Accounts/" + accounts[x] + "/statistic/" + "autoposting.pkl","wb"))		

# os.system("cls")
# count_of_threads = 0
# for c in range(len(threads)):
# 	count_of_threads += 1
# 	threads[c].start()
# 	print(count_of_threads)
# 	# time.sleep(30)
# 	# os.system('cls')