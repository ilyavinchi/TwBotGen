import pickle
import os
import telebot
import time

def logging(log_driver, log_path, take_screenshot, log_write, log_write_name, what_write):
	driver = log_driver
	if take_screenshot == 1:
		driver.save_screenshot(log_path + time.ctime(time.time()))

	if log_write == 1:
		if os.path.exists(log_path + log_write_name):
			with open(log_path + log_write_name, 'a') as f:
				f.write("\n" + time.ctime(time.time()) + " " + what_write)
		else:
			with open(log_path + log_write_name, 'w') as f:
				f.write(time.ctime(time.time()) + " " + what_write)
def pload(pload_path):
	while True:
		try:
			with open(pload_path, "rb") as f:
				return pickle.load(f)	
		except:
			time.sleep(1)
			continue
def pdump(pdump_path, what_dump):
	while True:
		try:
			with open(pdump_path, "wb") as f:
				pickle.dump(what_dump, f)			
			return True
		except:
			time.sleep(1)
			continue
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

bot = telebot.TeleBot('1107563794:AAHwpuyWE1JWF2ZLTfGp7pMnMmWX_ys8omw')
@bot.message_handler(commands=['start'])
def start_message(message):
	accounts = os.listdir("Accounts/")
	for x in range(len(accounts)):
		bot.send_message(message.chat.id, accounts[x] + " [" + str(x) + "]")
	
@bot.message_handler(content_types=['text'])
def send_text(message):
	accounts = os.listdir("Accounts/")
	if message.text.lower() == "cmds":
		bot.send_message(message.chat.id, "all")
		bot.send_message(message.chat.id, "timers")
		bot.send_message(message.chat.id, "logs wait")
		bot.send_message(message.chat.id, "logs newaccounts")
		bot.send_message(message.chat.id, "number 0 - " + str(len(accounts)))

	if message.text.lower() == "timers":
		for x in accounts:
			a = pload("Accounts/" + x + "/settings/timers.pkl")
			string_send = x + "\nNext start posting: " + time.ctime(a[0] + 7200)  + "\nNext start subscribe: " + time.ctime(a[1] + 7200)
			bot.send_message(message.chat.id, string_send)

	if message.text.isdigit() and int(message.text) < len(accounts):
		try:
			autoposting_statistic = pickle.load(open("Accounts/" + accounts[int(message.text)] + "/statistic/" + "autoposting.pkl", "rb"))
			autosubscribe_statistic = pickle.load(open("Accounts/" + accounts[int(message.text)] + "/statistic/" + "autosubscribe.pkl", "rb"))
			mess = "BOTNAME: " + accounts[int(message.text)] + " [" + str(int(message.text)) + "]" + "\nAUTOPOSTING STAT:" + "\nstatus: " + autoposting_statistic[0] + "\nposts: " + str(autoposting_statistic[1]) + "/" + str(autoposting_statistic[2]) + "\nNext post: " + autoposting_statistic[3] + "\nAUTOSUBSCRIBE STAT:" + "\nstatus: " + autosubscribe_statistic[0] + "\ncount: " + str(autosubscribe_statistic[1]) + "/" + str(autosubscribe_statistic[2])
			bot.send_message(message.chat.id, mess)
		except:
			pass

	if message.text.lower() == "all":
		for x in range(len(accounts)):
			try:
				autoposting_statistic = pickle.load(open("Accounts/" + accounts[x] + "/statistic/" + "autoposting.pkl", "rb"))
				autosubscribe_statistic = pickle.load(open("Accounts/" + accounts[x] + "/statistic/" + "autosubscribe.pkl", "rb"))
				mess = "BOTNAME: " + accounts[x] + " [" + str(x) + "]" + "\nAUTOPOSTING STAT:" + "\nstatus: " + autoposting_statistic[0] + "\nposts: " + str(autoposting_statistic[1]) + "/" + str(autoposting_statistic[2]) + "\nNext post: " + autoposting_statistic[3] + "\nAUTOSUBSCRIBE STAT:" + "\nstatus: " + autosubscribe_statistic[0] + "\ncount: " + str(autosubscribe_statistic[1]) + "/" + str(autosubscribe_statistic[2])
				bot.send_message(message.chat.id, mess)	
			except:
				pass

	if message.text.lower() == "logs wait":
		try:
			with open('Accounts_logs/Wait/waitlogs.txt', 'rb') as f:
				doc = f
			bot.send_document(message.chat.id, doc)
			bot.send_document(message.chat.id, "FILEID")
		except:
			bot.send_message(message.chat.id, "Wait logs doesn't exist")	

	if message.text.lower() == "logs newaccounts":
		try:
			new_accounts = os.listdir("Accounts_logs/NewAccounts")
			for x in new_accounts:
				with open('Accounts_logs/NewAccounts/' + x, 'rb') as f:
					bot.send_document(message.chat.id, f)
					bot.send_document(message.chat.id, "FILEID")
		except:
			# bot.send_message(message.chat.id, "NewAccounts logs doesn't exist")
			pass

bot.polling()
	