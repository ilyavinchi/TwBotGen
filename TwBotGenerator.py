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
from shutil import move

def diedthread(*diedthread_args):
	pass
works = True
next_thread = False
offer_link = "http://wait3seconds.ga/"

max_threads = 10
active_threads = [Thread(target=diedthread, args=("1")) for c in range(max_threads)]
pause_time = 86400

default_limit_subscribes = 300
default_start_interval = 60
default_end_interval = 90
default_parsing_limit = 5
default_sendtext = "(nude OR sex OR tits)"

default_limit_posts = 5
default_interval_between_posts = 2 * 60 * 60

def stat(*stat_args):
	import TwitterBotStatistic
Thread(target=stat, args=("1")).start()

def logging(log_driver, log_path, take_screenshot, log_write, log_write_name, what_write):
	driver = log_driver
	if take_screenshot == 1:
		driver.save_screenshot(log_path + time.ctime(time.time()))

	if log_write == 1:
		if os.path.exists(log_path + log_write_name + ".txt"):
			with open(log_path + log_write_name + ".txt", 'a') as f:
				f.write("\n" + time.ctime(time.time()) + " " + what_write)
		else:
			with open(log_path + log_write_name + ".txt", 'w') as f:
				f.write(time.ctime(time.time()) + " " + what_write)
def wait(dr, el_info, tries, wait_type):
	if wait_type == 1:
		for x in range(tries*10):
			try:
				elem = dr.find_element(By.XPATH, el_info)
				return elem
			except:
				time.sleep(0.1)
	elif wait_type == 2:
		for x in range(tries*10):
			try:
				elem = dr.find_elements(By.XPATH, el_info)
				return elem
			except:
				time.sleep(0.1)

	logging(0, 'Accounts_logs/Wait/', 0, 1, 'waitlogs', "ERROR " + el_info)
	# print("ERROR " + el_info)
	elem = 1/0
	return False
def pload(pload_path):
	if os.path.exists(pload_path):
		while True:
			try:
				with open(pload_path, "rb") as f:
					return pickle.load(f) 
			except:
				time.sleep(1)
				continue
	else:
		a = 1/0
def pdump(pdump_path, what_dump):
	if os.path.exists(pdump_path):
		while True:
			try:
				with open(pdump_path, "wb") as f:
					pickle.dump(what_dump, f)     
				return True
			except:
				time.sleep(1)
				continue
	else:
		a = 1/0
def changearrayval(changefile_path, change_key, change_val):
	while True:
		try:
			filearray = pload(changefile_path)
			filearray[change_key] = change_val
			pdump(changefile_path, filearray)
			break
		except:
			time.sleep(1)
			continue

accounts = os.listdir("Accounts/")
accounts_names = {}
# for x in accounts:
# print(pload("Accounts/" + x + "/statistic/autoposting.pkl"))

for x in accounts:
	pdump("Accounts/" + x + "/settings/timers.pkl", [1,1])
	print(pload("Accounts/" + x + "/settings/timers.pkl"))
	a_statistic = ["OFF",0, 0]
	pickle.dump( a_statistic , open("Accounts/" + x + "/statistic/" + "autosubscribe.pkl","wb"))
	p_statistic = ["OFF",0, 0, "-"]
	pickle.dump( p_statistic , open("Accounts/" + x + "/statistic/" + "autoposting.pkl","wb"))  

def test_accounts():
	print(accounts)
	for x in accounts:
		driver = driver_start(x, False)
		os.system("cls")
		print(pload("Accounts/" + x + "/settings/enter.pkl"))
		time.sleep(5)
		if driver.current_url == "https://twitter.com/account/access":
			access(driver, x)
		input("NEXT?: ", )
		driver.quit()

def driver_start(bot_name, headless_mode):
	options = Options()
	headless = headless_mode
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
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

def access(access_driver, access_name):
	print("Access START")
	driver = access_driver
	enter = pload('Accounts/' + access_name + '/settings/enter.pkl')
	send_msg = True
	for x in range(900):
		if wait(driver, "//input[@id='code']", 1, 2):
			break
		else:
			if send_msg:
				bot = telebot.TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
				bot.send_message(457184560, "Введи рекапчу\n" + "Login: " + enter[0] + "\nPassword: " + enter[1])
				send_msg = False
			driver.refresh()
			time.sleep(2)
			continue

		bot = telebot.TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
		bot.send_message(457184560, "Время ввышло")
		driver.quit()
		return "p"
		
	with open('Accounts/' + access_name + '/settings/enter.pkl', 'rb') as f:
		enter = pickle.load(f)
	if enter[2]:
		for n in range(1200):
			if works:
				enter_info = requests.get('http://api.sms-reg.com/getNumRepeat.php?tzid=' + enter[2] + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
				enter_info = enter_info.text
				json_enter_info = json.loads(enter_info)
				print(int(json_enter_info['response']))
				if int(json_enter_info['response']) == 0:
					driver.quit()
					return False
				elif int(json_enter_info['response']) == 1:
					wait(driver, "//input[@id='code']", 10, 1).send_keys(sms_get(json_enter_info['tzid']))
					requests.get('http://api.sms-reg.com/setOperationOk.php?tzid=' + json_enter_info['tzid'] + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
					wait(driver, "//input[@type='submit']", 10, 1).click()
					return True
				elif int(json_enter_info['response']) == 2:
					driver.quit()
					return False
				elif int(json_enter_info['response']) == 3:
					time.sleep(1)
			else:
				return True
		driver.quit()
		return False

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
	link_to_shorter = offer_link
	wait(driver, '//input[@class="urlbox"]', 10, 1).send_keys(link_to_shorter)
	wait(driver, "//div[@id='shorturllabel']/label", 10, 1).click()

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
	time.sleep(2)
	# while wait(driver, "//input[@id='short_url']", 10, 2).textst != ("https://is.gd/" + link_save):
	#   time.sleep(0.1)
	driver.quit()
	return "https://is.gd/" + link_save

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
	link_to_shorter = offer_link
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
	time.sleep(2)
	driver.quit()
	return " https://is.gd/" + link_save

def parsing_first_type(dr, send_parsing_text, p_l):
	driver = dr
	driver.get("https://twitter.com/search")
	el = wait(driver, "//input[@data-testid='SearchBox_Search_Input']", 10, 1)
	el.click()
	el.send_keys(send_parsing_text)
	time.sleep(2)
	wait(driver, "//div[@id='typeaheadDropdown-1']/div[2]", 10, 1).click()
	time.sleep(2)
	driver.get(wait(driver, "//div[@role='tablist']/div[2]/a", 10, 1).get_attribute("href"))
	driver.refresh()
	time.sleep(2)
	for x in range(30):
		try:
			logins = wait(driver, "//div[@dir='ltr']/span", 10, 2)
			ready_logins = []
			for i in range(p_l):
				ready_logins.append(logins[i].text.replace("@", ""))
			return ready_logins
		except:
			driver.refresh()
			time.sleep(1)
			print("PARSING ERROR")
			continue

def autoposting_start(botname_posting, countofposts, pause_between_posts):
	global next_thread
	a_s = [botname_posting, countofposts, pause_between_posts]
	list_of_images = os.listdir("Accounts/" + a_s[0] + "/imgs/")
	count_of_posts = 0
	error_tries = 0
	while count_of_posts < a_s[1] and works:
		try:
			driver = driver_start(a_s[0], False)
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "~_~_~_~_~_~_~_~_~" + a_s[0] + "~_~_~_~_~_~_~_~_~")
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "START")
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "TRY CLICK: Direct Messages")
			wait(driver, '//a[@aria-label="Direct Messages"]', 60, 1).click()
			try:
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "BAN CHECK")
				wait(driver, '//div[@role="alert"]', 3, 1)
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "BAN FIND")
				changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, False)
				changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 1, False)
				next_thread = False
				driver.quit()
				return False
			except:
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "NOT BANNED")
				pass

			driver.get("https://twitter.com/home")
			time.sleep(1)
			driver.refresh()
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "START POSTING")
			random_number_for_image = r.randint(0, len(list_of_images) - 1)
			all_texts = open("Accounts_lists/texts.txt", 'r', encoding="utf-8").read().split("\n\n")
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "TRY GET SHORT URL")
			contents_from_file = all_texts[r.randint(0, len(all_texts) - 1)] + url_shortener_sec(a_s[0])
			clipboard.copy(contents_from_file)
			el = wait(driver, "//div[@class='notranslate public-DraftEditor-content']", 10, 1)
			el.click()
			el.send_keys(Keys.CONTROL, 'v')
			time.sleep(2)
			wait(driver, "//input[@type='file']", 10, 1).send_keys(os.path.abspath("Accounts/" + a_s[0] + "/imgs/" + list_of_images[random_number_for_image]))
			time.sleep(5)
			wait(driver, "//div[@data-testid='tweetButtonInline']", 10, 1).send_keys(Keys.ENTER)
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "POST ADD: " + str(count_of_posts) + "/" + str(a_s[1]))
			time.sleep(5)
			count_of_posts += 1
			driver.quit()
			next_thread = False
			if count_of_posts < a_s[1]:		
				time_next_post = time.ctime(time.time() + a_s[2]).split(" ")[3]
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "TIME TO NEXT POST: " + str(time_next_post))
				autoposting_statistic = ["WORKING", count_of_posts, a_s[1], time_next_post]
				pickle.dump( autoposting_statistic , open("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl","wb"))
				for x in range(a_s[2]):
					if works:
						time.sleep(1)
					else:
						next_thread = False
						changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, time.time() + pause_time)
						autoposting_statistic = ["END WORK",count_of_posts, a_s[1], "--:--:--"]
						pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
						return False
			else:
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "WORK END")
				changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, time.time() + pause_time)
				autoposting_statistic = ["END WORK",count_of_posts, a_s[1], "--:--:--"]
				pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
				return False
			error_tries = 0
		except Exception as e:
			logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "ERROR")
			next_thread = False
			print(e)
			if driver.current_url == "https://twitter.com/account/access":
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "WAIT ACCES")
				access_res = access(driver, a_s[0])
				autoposting_statistic = ["Wait ACCESS", 0, 0, "-"]
				pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
				if access_res == "p":
					logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "PAUSE")
					changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, time.sleep() + 14400)
					changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 1, time.sleep() + 14400)
					autoposting_statistic = ["ERROR", 0, 0, "-"]
					pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
					driver.quit()
					return False
				elif access_res:
					logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "ACCESS ACCEPT")
					continue
				else:
					logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "ACCOUNT BANNED")
					autoposting_statistic = ["ERROR", 0, 0, "-"]
					pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
					changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, False)
					changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 1, False)
					driver.quit()
					return False
			if error_tries < 3:
				driver.quit()
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "RETRY: " + str(error_tries))
				error_tries += 1
			else:
				logging(driver, 'Accounts_logs/Autoposting/', 0, 1, a_s[0], "COMPLETELY ERROR: " + e)
				driver.quit()
				autoposting_statistic = ["ERROR", 0, 0, "-"]
				pdump("Accounts/" + a_s[0] + "/statistic/" + "autoposting.pkl", autoposting_statistic)
				changearrayval('Accounts/' + a_s[0] + '/settings/timers.pkl', 0, time.time() + pause_time)
				return False

def autosubscribe_start(botname_subscribe, limitsubscribes, startinterval, endinterval, sendtext, parsinglimit):
	global next_thread
	s_s = [botname_subscribe, limitsubscribes, startinterval, endinterval, sendtext, parsinglimit]
	driver = driver_start(s_s[0], True)
	logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "~_~_~_~_~_~_~_~_~" + s_s[0] + "~_~_~_~_~_~_~_~_~")
	for x in range(6):
		try:
			logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "TRY CLICK PROFILE")
			wait(driver, '//a[@aria-label="Profile"]', 10, 1).click()
			break
		except:
			if driver.current_url == "https://twitter.com/account/access":
				logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS")
				access_res = access(driver, s_s[0])
				autosubscribe_statistic = ["WAIT ACCESS",0, 0]
				pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
				if access_res == "p":
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS PAUSE")
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, time.sleep() + 14400)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.sleep() + 14400)
					autosubscribe_statistic = ["ERROR",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					driver.quit()
					next_thread = False
					return False
				elif access_res:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS SUCCES")
					next_thread = False
					continue
				else:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "BOT BANNED")
					autosubscribe_statistic = ["ERROR",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, False)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, False)
					driver.quit()
					next_thread = False
					return False
			continue
		next_thread = False
		return False
	
	time.sleep(5)
	try:
		following_count = int(wait(driver, '//div[1]/a/span/span', 10, 1).text)
	except:
		print("ERROR FOLLOWING COUNT")
		following_count = 0
	
	next_thread = False
	if following_count < 4000:
		logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "START FOLLOWING")
		subscribe_base = []
		if os.path.exists("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl"):
			subscribe_base = pload("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl")
		else:
			subscribe_base = []

		count_of_realsubscribe = 0
		error_tries = 0
		while count_of_realsubscribe != s_s[1]:
			try:   
				logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "TRY FOLLOWING")
				if len(subscribe_base) == 0:
					subscribe_base = parsing_first_type(driver, s_s[4], s_s[5])
					pdump("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl", subscribe_base)
					time.sleep(r.randint(s_s[2], s_s[3]))

				driver.get("https://twitter.com/" + subscribe_base[0])
				try:
					wait(driver, "//div[@data-testid='placementTracking']", 60, 1).click()
				except:
					if driver.current_url == "https://twitter.com/account/access":
						a = 1/0

				try:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "FIND ALLERT")
					wait(driver, '//div[@role="alert"]', 3, 1)
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ALLERT")
					autosubscribe_statistic = ["ERROR",count_of_realsubscribe, s_s[1]]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
					driver.quit()
					return False
				except:
					pass

				count_of_realsubscribe += 1
				subscribe_base.pop(0)
				pdump("Accounts/" + s_s[0] + "/databases/subscribe_base.pkl", subscribe_base)

				if not works:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "STOP WORK")
					autosubscribe_statistic = ["END WORK",count_of_realsubscribe, s_s[1]]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
					driver.quit()
					return False

				if (count_of_realsubscribe != s_s[1] and len(subscribe_base) != 0):
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "SUCCES END SUB " + str(count_of_realsubscribe) + "/" + str(s_s[1]))
					autosubscribe_statistic = ["WORKING",count_of_realsubscribe, s_s[1]]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					time.sleep(r.randint(s_s[2], s_s[3]))
				else:
					if count_of_realsubscribe != s_s[1]:
						logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "PARSING")
						autosubscribe_statistic = ["Parsing",count_of_realsubscribe, s_s[1]]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					else:
						logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "END WORK")
						autosubscribe_statistic = ["END WORK",count_of_realsubscribe, s_s[1]]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
						driver.quit()
						return False
				error_tries = 0
			except Exception as e:
				logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ERROR " + e)
				next_thread = False
				print(e)
				if driver.current_url == "https://twitter.com/account/access":
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS")
					access_res = access(driver, s_s[0])
					autosubscribe_statistic = ["WAIT ACCESS",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					if access_res == "p":
						logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS PAUSE")
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, time.sleep() + 14400)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.sleep() + 14400)
						autosubscribe_statistic = ["ERROR",0, 0]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
						driver.quit()						
						return False
					elif access_res:
						logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ACCESS SUCCES")
						next_thread = False
					else:
						logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "BOT BANNED")
						autosubscribe_statistic = ["ERROR",0, 0]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, False)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, False)
						driver.quit()						
						return False
				if error_tries < 3:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "ERROR TRIES: " + str(error_tries))
					error_tries += 1
					continue
				else:
					logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "TRIES END")
					autosubscribe_statistic = ["ERROR",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)	
					driver.quit()				
					return False
	else:
		logging(driver, 'Accounts_logs/Autosubscribe/', 0, 1, s_s[0], "START UNFOLLOWING")
		count_of_desubscribe = 0 
		driver.get(driver.current_url + "/following")
		error_tries = 0
		while (count_of_desubscribe < 350):
			try:
				followings = wait(driver, '//div[@aria-label="Timeline: Following"]/div/div/div/div/div/div/div/div/div/div/div/span/span', 10, 2)
				if works:
					for x in range(len(followings)):
						if works:
							try:
								if followings[x].text == "Following":
									followings[x].click()
									wait(driver, '//div[@data-testid="confirmationSheetConfirm"]', 10, 1).click()
									count_of_desubscribe += 1
									autosubscribe_statistic = ["DESUBSCRIBING", count_of_desubscribe, s_s[1]]
									pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
									time.sleep(r.randint(s_s[2], s_s[3]))
							except:
								if driver.current_url == "https://twitter.com/account/access":
									access_res = access(driver, s_s[0])
									autosubscribe_statistic = ["WAIT ACCESS",0, 0]
									pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
									if access_res == "p":
										changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, time.sleep() + 14400)
										changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.sleep() + 14400)
										autosubscribe_statistic = ["ERROR",0, 0]
										pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
										driver.quit()
										next_thread = False
										return False
									elif access_res:
										next_thread = False
									else:
										autosubscribe_statistic = ["ERROR",0, 0]
										pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
										changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, False)
										changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, False)
										driver.quit()
										next_thread = False
										return False           
								continue
						else:
							autosubscribe_statistic = ["END DESUBSCRIBE", count_of_desubscribe, s_s[1]]
							pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
							changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
							driver.quit()
							return False
					if len(followings) > 0:
						driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
				else:
					autosubscribe_statistic = ["END DESUBSCRIBE", count_of_desubscribe, s_s[1]]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
					driver.quit()
					return False
			except Exception as e:
				print(e)
				next_thread = False
				if driver.current_url == "https://twitter.com/account/access":
					access_res = access(driver, s_s[0])
					autosubscribe_statistic = ["WAIT ACCESS",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					if access_res == "p":
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, time.sleep() + 14400)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.sleep() + 14400)
						autosubscribe_statistic = ["ERROR",0, 0]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
						driver.quit()
						return False
					elif access_res:
						pass
					else:
						autosubscribe_statistic = ["ERROR",0, 0]
						pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 0, False)
						changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, False)
						driver.quit()
						return False
				if error_tries < 3:
					error_tries += 1
				else:
					autosubscribe_statistic = ["ERROR",0, 0]
					pdump("Accounts/" + s_s[0] + "/statistic/" + "autosubscribe.pkl", autosubscribe_statistic)
					changearrayval('Accounts/' + s_s[0] + '/settings/timers.pkl', 1, time.time() + pause_time)
					driver.quit()
					return False

def first_post(botname_post, first_url):
	list_of_images = os.listdir("Accounts/" + botname_post + "/imgs/")
	driver = driver_start(botname_post, False)
	driver.get("https://twitter.com/home")
	random_number_for_image = r.randint(0, len(list_of_images) - 1)
	all_texts = open("Accounts_lists/texts.txt", 'r', encoding="utf-8").read().split("\n\n")
	contents_from_file = all_texts[r.randint(0, len(all_texts) - 1)] + first_url
	clipboard.copy(contents_from_file)
	el = wait(driver, "//div[@class='notranslate public-DraftEditor-content']", 10, 1)
	el.click()
	el.send_keys(Keys.CONTROL, 'v')
	time.sleep(2)
	wait(driver, "//input[@type='file']", 10, 1).send_keys(os.path.abspath("Accounts/" + botname_post + "/imgs/" + list_of_images[random_number_for_image]))
	time.sleep(5)
	wait(driver, "//div[@data-testid='tweetButtonInline']", 10, 1).send_keys(Keys.ENTER)
	time.sleep(5)
	driver.quit()
	return True

def pin_post(pin_bot_name, pin_login):
	driver = driver_start(pin_bot_name, False)
	driver.get("https://twitter.com/" + pin_login)
	wait(driver, "//div[@data-testid='caret']", 10, 1).click()
	wait(driver, "//div[@data-testid='pin']", 10, 1).click()
	wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 10, 1).click() 
	time.sleep(3)
	driver.quit()

def phone_gen():
	phone_numb_search = requests.get('http://api.sms-reg.com/getNum.php?country=ru&service=twitter&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
	phone_numb_search = phone_numb_search.text
	json_phone_numb_search = json.loads(phone_numb_search)
	response_phone_numb_search = json_phone_numb_search['response']
	phone_search_tzid = json_phone_numb_search['tzid']
	for x in range(900):
		phone_numb_info = requests.get('http://api.sms-reg.com/getState.php?tzid=' + phone_search_tzid + '&apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
		phone_numb_info = phone_numb_info.text
		json_phone_numb_info = json.loads(phone_numb_info)
		if json_phone_numb_info['response'] == 'WARNING_NO_NUMS':
			return False, False
		elif json_phone_numb_info['response'] == 'TZ_INPOOL':
			time.sleep(1)
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
	print("TRY GEN NEW BOT")
	options = Options()
	headless = False
	if headless:
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
	options.add_argument('-–incognito')
	options.add_argument("--disable-notifications")
	options.add_argument("--disable-extensions")
	driver = webdriver.Chrome("chromedriver.exe", options = options)
	driver.set_window_size(1366, 768) if headless == True else driver.maximize_window() 

	driver.get("https://www.coedcherry.com/models/random")
	pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 2)
	while len(pictures) < 6:
		driver.get("https://www.coedcherry.com/models/random")
		pictures = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 2)

	model_name = driver.find_element(By.XPATH, "//h1").text
	model_name = model_name.split(' ')[0] + " " + model_name.split(' ')[1]
	logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "~-~-~-~-~-~-~-~-~-~-BOT NAME: " + model_name + "-~-~-~-~-~-~-~-~-~-~")
	
	try:
		os.mkdir("Accounts/" + model_name)
		os.mkdir("Accounts/" + model_name + "/imgs")
		logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Gen imgs")
		pictures_href = []
		for x in range(6):
			pictures_href.append(pictures[x].get_attribute("href"))

		for x in range(6):
			driver.get(pictures_href[x])
			pictures_second = wait(driver, "//div[@class='thumbs ']/figure/a", 10, 2)
			
			for z in range(len(pictures_second)):
				with open("Accounts/" + model_name + "/imgs/" + str(uuid.uuid1()).replace("-", "")[:10] + ".jpg", 'wb') as file:
					file.write(requests.get(pictures_second[z].get_attribute("href")).content)

		logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Try get phone")
		phone, phone_tzid = phone_gen()
		if phone:
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Get phone")
			driver.get("https://twitter.com/i/flow/signup")
			for x in range(6):
				try:
					wait(driver, "//input[@type='text']", 10, 1).send_keys(model_name)
					wait(driver, "//input[@type='tel']", 10, 1).send_keys(phone)
					break
				except:
					continue
				a = 1/0

			wait(driver, "//div[@role='group']/div/div/div[1]/div/select/option[@value='" + str(r.randint(1,12))+"']", 10, 1).click()
			wait(driver, "//div[@role='group']/div/div/div[2]/div/select/option[@value='" + str(r.randint(1,28))+"']", 10, 1).click()
			wait(driver, "//div[@role='group']/div/div/div[3]/div/select/option[@value='" + str(r.randint(1996,2001))+"']", 10, 1).click()

			for x in range(60):
				try:
					wait(driver, "//div[@data-testid='confirmationSheetConfirm']", 1, 1).click()
					break
				except:
					try:
						wait(driver, "//div/span/span", 1, 1).click()
					except:
						continue
				a = 1/0

			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Try get code")
			code = sms_get(phone_tzid)
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Code get")
			if code == 0:
				logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Code not get")
				rmtree("Accounts/" + model_name)
				a = 1/0
			wait(driver, "//input[@name='verfication_code']", 10, 1).send_keys(code)
			wait(driver, "//div/div/div/div[@role='button']/div/span/span", 10, 1).click()
			acc_password = "WWW2714070" + list(model_name)[0]
			wait(driver, "//input[@name='password']", 10, 1).send_keys(acc_password)
			for x in range(60):
				try:
					wait(driver, "//div/div/div/div[@role='button']/div/span/span", 1, 1).click()
					time.sleep(1)
					continue
				except:
					break
				a = 1/0
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Account create")        
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
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Files Add")
			split_name = model_name.split(" ")
			driver.get("https://twitter.com/settings/screen_name")
			try_combinations = [split_name[0] + split_name[1], split_name[1] + split_name[0], split_name[1] +"_"+ split_name[0], split_name[0] +"_"+ split_name[1], split_name[1] + split_name[0] + "_", split_name[0] + split_name[1] + "_", split_name[0] + "_" + split_name[1] + "_", split_name[1] + "_" + split_name[0] + "_"]
			last_login = ''
			login = ''
			time.sleep(10)
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Try change name")
			for x in range(8):
				if driver.current_url == "https://twitter.com/settings/screen_name":
					try:
						while wait(driver, "//input", 10, 1).get_attribute("value") != "":
							wait(driver, "//input", 10, 1).send_keys(Keys.BACK_SPACE)
						wait(driver, "//input", 10, 1).send_keys(try_combinations[x])
						wait(driver, '//div[@data-testid="settingsDetailSave"]', 10, 1).click()
						time.sleep(2)
					except:
						break
				else:
					break
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Name change")
			time.sleep(5)
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Try change language")
			login = wait(driver, "//div[@role='tablist']/div/h2", 10, 1).text
			driver.get("https://twitter.com/settings/language")
			wait(driver, "//option[@value='en']", 10, 1).click()
			wait(driver, "//div/div/div/span/span", 10, 1).click()
			driver.refresh()
			time.sleep(2)
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Language change")
			driver.get("https://twitter.com/settings/country")
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Try change country")
			wait(driver, "//option[@value='us']", 10, 1).click()
			wait(driver, "//div[@aria-haspopup='false'][1]", 10, 1).click()
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Country change")
			time.sleep(2)
			driver.get("https://twitter.com/" + login)

			driver.get("https://twitter.com/settings/profile")
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Changing avatars")
			list_of_images = os.listdir("Accounts/" + model_name + "/imgs/")
			im = ''
			for x in range(len(list_of_images)):
				im = Image.open("Accounts/" + model_name + "/imgs/" + list_of_images[x])
				w, h = im.size
				if w > h:
					im = list_of_images[x]
					break

				im = list_of_images[r.randint(0, len(list_of_images) - 1)]
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Making descriprion")
			wait(driver, "//div[1]/div[1]/div/div/div/input[@type='file']", 10, 1).send_keys(os.path.abspath("Accounts/" + model_name + "/imgs/" + im))
			wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			random_number_for_image = r.randint(0, len(list_of_images) - 1)
			wait(driver, "//div[1]/div[2]/div/div/div/input[@type='file']", 10, 1).send_keys(os.path.abspath("Accounts/" + model_name + "/imgs/" + list_of_images[random_number_for_image]))
			wait(driver, "//div[2]/div[1]/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			url = url_shortener_main(model_name)
			wait(driver, "//textarea[@name='description']", 10, 1).send_keys("Register and find me here - " + url)
			wait(driver, "//input[@name='url']", 10, 1).send_keys(url)
			wait(driver, "//div[1]/div/div/div/div/div/div/div/div/div/div/div/div/span/span", 10, 1).click()
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Create pin post")
			try:
				first_post(model_name, url)
				pin_post(model_name, login)
			except:
				logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "ERROR: NOT PIN")
			
			pdump("Accounts/" + model_name + "/settings/enter.pkl", [login, acc_password, phone_tzid])
			pdump("Accounts/" + model_name + "/settings/timers.pkl", [1,1])
			balance_info = requests.get('http://api.sms-reg.com/getBalance.php?apikey=8t0kjwxk118uih3peiw3c8rbb7e61g62')
			balance_info = balance_info.text
			json_balance_info = json.loads(balance_info)
			bot = telebot.TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
			bot.send_message(457184560, "Ваш балланс: " + json_balance_info['balance'])
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "~-~-~-~-~-~-~-~-~-~-Complete making bot-~-~-~-~-~-~-~-~-~-~\n")
			driver.quit()
			return model_name
		else:
			driver.quit()
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Phone not get")
			rmtree("Accounts/" + model_name)
			return False
	except:
			driver.quit()
			print("GEN NEW ERROR")
			logging(0, 'Accounts_logs/NewAccounts/', 0, 1, model_name, "Phone not get")
			rmtree("Accounts/" + model_name)
			return False    

while works:
	for x in range(max_threads):
		print("THREAD ID: " + str(x))
		if not active_threads[x].is_alive():
			print("START NEW AUTOPOSTING")
			while next_thread:
				time.sleep(1)
			next_thread = True
			thread_name = False
			auto_type = False
			accounts = os.listdir("Accounts/")
			for q in accounts:
				timers = pload("Accounts/" + q + "/settings/timers.pkl")
				if timers[0] and timers[0] != "+" and timers[0] < time.time():
					thread_name = q
					auto_type = 0
					changearrayval("Accounts/" + q + "/settings/timers.pkl", 0, "+")
					break
				elif timers[1] and timers[1] != "+" and timers[1] < time.time():
					thread_name = q
					auto_type = 1
					changearrayval("Accounts/" + q + "/settings/timers.pkl", 1, "+")
					break

			while not thread_name:
				try:
					print("START NEW ACCOUNT GEN")
					thread_name = account_gen()
				except:
					continue  
				auto_type = 0

			if auto_type == 0:
				print("START NEW AUTOPOSTING")
				changearrayval("Accounts/" + q + "/settings/timers.pkl", 0, "+")
				active_threads[x] = Thread(target=autoposting_start, args=(thread_name, default_limit_posts, default_interval_between_posts))
				active_threads[x].start()
			elif auto_type == 1:
				print("START NEW AUTOSUBSCRIBE")
				changearrayval("Accounts/" + q + "/settings/timers.pkl", 1, "+")
				active_threads[x] = Thread(target=autosubscribe_start, args=(thread_name, default_limit_subscribes, default_start_interval, default_end_interval, default_sendtext, default_parsing_limit))
				active_threads[x].start()

	accounts_list = os.listdir("Accounts/")
	for x in accounts_list:
		timers = pload("Accounts/" + x + "/settings/timers.pkl")
		if not timers[0] and not timers[1]:
			while next_thread:
				time.sleep(1)
			pload("Accounts/" + x + "/settings/timers.pkl")
			move('Accounts/' + x, "Accounts_banned/" + x)
	time.sleep(30)

# if works:
#   Thread(target=autoposting_updater, args=("1")).start()
#   Thread(target=autosubscribe_updater, args=("1")).start()
#   Thread(target=banned_updater, args=("1")).start()

# while True:
#   commands = ''
#   with open("t.cmds", 'r') as f:
#     commands = f.read()
#   if commands:
#     if commands == '1':
#       works = False
#       print(autosubscribe_threads)
#       print(autoposting_threads)
#     elif commands == '2':
#       os.system("cls")
#     elif commands == '3':
#       accounts_list = os.listdir("Accounts/")
#       for x in accounts_list:
#         print(x, pload("Accounts/" + x + "/settings/timers.pkl"))
#     with open("t.cmds", 'w') as f:
#       f.write("")
#   time.sleep(5)
