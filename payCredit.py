from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class Pay():

	def __init__(self):
		client = MongoClient()
		self.db = client.cards
		self.debit = self.db.cards.find_one({'card': 'debit'})
		self.credit = self.db.cards.find_one({'card': 'credit'})
		self.credit_needed_to_pay = 0
		

	def getCredit(self):
		driver = webdriver.PhantomJS()
		driver.get(self.credit['website'])

		user = driver.find_element_by_id('username')
		user.send_keys(self.credit['username'])
		print 'sent in user credentials'

		password = driver.find_element_by_id('password')
		password.send_keys(self.credit['password'])
		print 'sent in password'

		driver.find_element_by_css_selector("form[name='logonForm'] input[type='submit']").click()
		print 'submitting username and password'
		
		if driver.find_element_by_xpath("//div[@class='module-header']/h2"):
			print 'secret needed'
			secret = driver.find_element_by_id('hintanswer')
			secret.send_keys(self.credit['secret'])
			driver.find_element_by_css_selector("input[type='submit']").click()

		credit_num = driver.find_element_by_css_selector("div[class='value'] span[class='nowrap ']").text
		credit_num = float(credit_num.replace('$', ''))

		self.credit_needed_to_pay = credit_num
		return credit_num

	def getDebit(self):
		driver = webdriver.PhantomJS()
		print 'getting debit website'
		driver.get(self.debit['website'])
		# needed to load js
		print 'sleeping'
		time.sleep(5)
		print 'done sleeping'

		print 'inputting user'
		try:
			user = driver.find_element_by_xpath("//input[@type='text']")
			user.send_keys(self.debit['card_num'])
		except:
			driver.save_screenshot('user.png')
		print 'inputting password'

		try:
			password = driver.find_element_by_xpath("//input[@type='password']")
			password.send_keys(self.debit['password'])
		except:
			driver.save_screenshot('password.png')

		print 'pressing button'
		driver.find_element_by_xpath("//button[@type='submit']").click()

		print 'sleeping'
		time.sleep(5)
		print 'done sleeping'

		current_debit_balance = driver.find_element_by_xpath("//span[@class='category-balance']").text
		current_debit_balance = float(current_debit_balance.replace("$",""))

		if current_debit_balance > self.credit_needed_to_pay:
			driver.find_element_by_xpath("//a[@href='#/payments/new']").click()
			time.sleep(5)
			print 'entering into credit card input'
			need_to_pay = driver.find_element_by_xpath('//div[2]/fieldset/table/tbody/tr[2]/td[3]//ui-textbox//input')
			need_to_pay.send_keys(str(self.credit_needed_to_pay))
			print 'submitting the pay'
			driver.find_element_by_xpath("//button[@type='submit']").click()



if __name__ == '__main__':
	pay = Pay()
	print 'getting credit'
	credit = pay.getCredit()
	if credit >= 0:
		print 'getting debit'
		debit = pay.getDebit(0)


