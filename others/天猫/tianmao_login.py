# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 22:08
# @Author  : LGD
# @File    : tianmao_login.py
# @功能    :

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.action_chains import ActionChains

# browser = webdriver.Chrome()
# browser.get('https://www.tianmao.com')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)
driver.maximize_window()
print(driver.title)
comments_btn = driver.find_element_by_xpath('//*[@id="J_TabBar"]/li[2]/a')
comments_btn.click()
# comments_list = driver.find_elements_by_xpath('//*[@id="J_Reviews"]/div/div[6]/table/tr')
comments_list = driver.find_elements_by_xpath('//*[@id="J_Reviews"]/div/div[6]/table/tbody/tr')
pages = driver.find_element_by_xpath('//div[@class="rate-paginator"]/a[@data-page="2"]')
print(len(comments_list))
for i in comments_list:
    content = i.find_element_by_xpath('.//div[@class="tm-rate-fulltxt"]')
    time = i.find_element_by_xpath('.//div[@class="tm-rate-date"]')
    category = i.find_element_by_xpath('.//div[@class="rate-sku"]')
    print(content.get_attribute('textContent'))
    print(time.get_attribute('textContent'))
    print(category.get_attribute('textContent'))

# next_page = pages[-1]
# print(next_page.get_attribute('textContent'))
# driver.execute_script("arguments[0].scrollIntoView();", next_page)
# print(pages.location)
# ActionChains(driver).move_to_element(pages).click().perform()
# pages.click()



# browser.get('https://chaoshi.detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.54ed75b2z47SBm&id=523962011119&user_id=725677994&cat_id=2&is_b=1&rn=f20cec0049c884523d2a5bbc7cd6910f')
# iframe = WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, "sufei-dialog-content")))
# browser.switch_to.frame("sufei-dialog-content")
# account = browser.find_element_by_id('TPL_username_1')
# account.clear()
# account.send_keys('17839931230')
# password = browser.find_element_by_id('TPL_password_1')
# password.clear()
# password.send_keys('l19960202')
#
# login_btn = browser.find_element_by_id('J_SubmitStatic')
# print(element)

# WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, "sufei-dialog-close")))
# WebDriverWait(browser, 5, 0.5).until(EC.presence_of_element_located((By.ID, "J_TabBar")))
# element.click()

# close_btn = browser.find_element_by_id('J_TabBar')
# print(browser.page_source)
# close_btn.click()
# text = close_btn.get_attribute('textContent')
# print(text)

