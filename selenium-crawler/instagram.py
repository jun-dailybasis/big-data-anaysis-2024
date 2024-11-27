import pdb
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

LOGIN_URL = 'https://www.instagram.com/accounts/login'
LOGIN_ID = 'jjua.qq'
LOGIN_PW = 'qkd123123@@'

CRAWLING_URL ='https://www.instagram.com'


if __name__ == '__main__':
    browser = webdriver.Chrome()
    browser.get(LOGIN_URL)
    browser.implicitly_wait(3)

    elem = browser.find_element(By.NAME, 'username')
    elem.send_keys(LOGIN_ID)


    elem = browser.find_element(By.NAME, 'password')
    elem.send_keys(LOGIN_PW + Keys.ENTER)


    time.sleep(10) # 로그인 하고 즉각 되는게 아니니까 좀 기다리자.

    browser.get(CRAWLING_URL)

    # 로딩 기다리자
    time.sleep(3)


    for i in range(5):
        elem = browser.find_element(By.TAG_NAME, "html")
        elem.send_Keys(Keys.END)

        time.sleep(3)
        
    articles = browser.find_elements(By.TAG_NAME,'article')
    
    
    for x in articles:
        soup = BeautifulSoup(x.text, 'html.parser')
        print(soup)
        print()

    time.sleep(10)