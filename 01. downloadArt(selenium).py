import os
from selenium import webdriver
import requests

# Using Chrome to access web
driver = webdriver.Chrome('chromedriver(v80).exe')
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
# Open the website
url='https://www.ecosia.org/images?q='

def saveImage(iname,link):
    img_data = requests.get(link, headers=headers).content
    with open(iname+'.jpg', 'wb') as f:
        f.write(img_data)

def downloadImage(driver,url,query):
    q=query[:-4].replace(' ','+')+'&size=large'
    xpath='/html/body/div[1]/div/main/div[2]/div/a[1]/img'
    driver.get(url+q)

    link = driver.find_element_by_xpath(xpath).get_attribute("src")
    print(link)
    saveImage(query,link)

query = 'Usher  - U Got It Bad.mp3'
downloadImage(driver,url,query)
