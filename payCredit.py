from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_cards():
    client = MongoClient()
    db = client.cards

    credit = db.cards.find_one({'card':'credit'})
    debit = db.cards.find_one({'card':'debit'})

    return debit, credit


def find_credit_balance(credit):
    driver = webdriver.PhantomJS()

    driver.get(credit['website'])

    user = driver.find_element_by_id('username')
    user.send_keys(credit['username'])

    password = driver.find_element_by_id('password')
    password.send_keys(credit['password'])

    driver.find_element_by_xpath('//*[@id="content"]/div[3]/div[2]/form/div[2]'
                                 '/div[2]/input').click()
    if driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[1]/h2'):
        secret = driver.find_element_by_name('hintanswer')
        secret.send_keys(credit['secret'][0])
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/div[2]'
                                     '/form/div/div[3]/div/input').click()

    owing = driver.find_element_by_xpath(
        "//div[@class='balance']//div[@class='value']"
        ).text
    
    driver.close()
    print('You owe: '+ owing)
    return owing

if __name__ == '__main__':

    debit, credit = get_cards()
    owe = find_credit_balance(credit)
    #find_debit_balance(debit)






