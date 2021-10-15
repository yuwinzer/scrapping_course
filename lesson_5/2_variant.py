from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common import exceptions as se
from pymongo import MongoClient
from pprint import pprint
import time

# ///////////////////////
# /// selenium script ///
# ///////////////////////

chrome_options = Options()

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')
time.sleep(1)
try:
    elem_modal = driver.find_element(By.XPATH, "//mvid-icon[contains(@class, "
                                               "'modal-layout__close')]/*[name()='svg']/*[name()='use']")
    elem_modal.click()
except se.NoSuchElementException:
    pass


y_pos = 1000
for _ in range(3):
    time.sleep(1)
    driver.execute_script(f'window.scroll(0, {y_pos});')
    y_pos += 1000

target_block = driver.find_element(By.XPATH, "//mvid-shelf-group")
actions = ActionChains(driver)
actions.move_to_element(target_block)
actions.perform()

time.sleep(2)
button_popular = driver.find_element(By.XPATH, "//button[contains(@class, 'tab-button ng-star-inserted')]")
button_popular.click()

while True:
    try:
        time.sleep(1)
        button_next = driver.find_element(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/button[2]")
        button_next.click()
    except se.ElementNotInteractableException:
        break
    except se.ElementClickInterceptedException:
        break

all_goods = []

names = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/div/mvid-product-cards-group/"
                                       "div[contains(@class, 'product-mini-card__name ng-star-inserted')]/div/a")
prices = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/div/mvid-product-cards-group/"
                                        "div[contains(@class, 'product-mini-card__price ng-star-inserted')]/"
                                        "mvid-price-2/div/div[1]/span[1]")
ratings = driver.find_elements(By.XPATH, "//mvid-shelf-group/mvid-carousel/div/div/mvid-product-cards-group/"
                                       "div[contains(@class, 'product-mini-card__rating ng-star-inserted')]/"
                                         "mvid-plp-product-rating/a/mvid-star-rating/span")
goods = []
for i in range(len(names)):
    temp_dict = {}
    temp_dict['name'] = names[i].text
    temp_dict['link'] = names[i].get_attribute('href')
    temp_dict['price'] = int((prices[i].text).replace(' ',''))
    try:
        temp_dict['rating'] = float(ratings[i].text.replace(',','.'))
    except:
        temp_dict['rating'] = None
    goods.append(temp_dict)
pprint(goods)


# ///////////////////////////
# /// import into MongoDB ///
# ///////////////////////////

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}

# create mongo database
client = MongoClient('127.0.0.1', 27017)
db = client['mvideo']
trend_goods = db.trend_goods

trend_goods.delete_many({})  # get empty before start

for i in range(len(goods)):
    trend_goods.insert_one(goods[i])




