import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unicodedata
import json
import time
import uuid
import requests
import csv

def firebaseKey(key):
  newKey = key.replace('$', '_')
  newKey = newKey.replace('/', '_')
  newKey = newKey.replace('#', '_')
  newKey = newKey.replace(' ', '_')
  newKey = newKey.replace('.', '_')

  return newKey

def scrollWholePage(driver):
  SCROLL_PAUSE_TIME = 0.5

  # Get scroll height
  last_height = driver.execute_script("return document.body.scrollHeight")

  for i in range(100):
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# SET THE DRIVER
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-dev-shm-usage") # overcome limited resource problems
chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
driver = webdriver.Chrome(executable_path="chromedriver",   chrome_options=chrome_options)

# USE THE DRIVER
def lambda_handler(*args, **kwargs):
  driver.get('https://www.facebook.com/groups/SF4stay')
  scrollWholePage(driver)
  time.sleep(2)
  postContainers = driver.find_elements_by_class_name('mtm')

  with open('apts2.csv', 'wb') as csvfile:
    csvWriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for postContainer in postContainers:
      try:
        subPostContainer = postContainer.find_element_by_class_name('_l52')
        headerDiv = subPostContainer.find_element_by_tag_name('div')
        title = ''
        price = ''
        location = ''
        description = ''
        try:
          title = headerDiv.find_element_by_class_name('_l53').get_attribute('innerText')
        except:
          print 'title err'
        try:
          price = headerDiv.find_element_by_class_name('_l57').get_attribute('innerText')
        except:
          print 'price err'
        try:
          location = headerDiv.find_element_by_class_name('_l58').get_attribute('innerText')
        except:
          print 'location err'
        try:
          postContainer.find_element_by_class_name('see_more_link').click()
        except:
          print ''
        try:
          descriptionContainer = postContainer.find_element_by_class_name('text_exposed_root')
          line = descriptionContainer.find_element_by_tag_name('p').get_attribute('innerText')
          description = description + line
        except:
          print 'description1 err'
        try:
          descriptionContainer = postContainer.find_element_by_class_name('text_exposed_show')
          line = descriptionContainer.find_element_by_tag_name('p').get_attribute('innerText')
          description = description + line
        except:
          print 'description2 err'
        # print title + price + location
        csvWriter.writerow([ title, price, location, description ])
      except:
        print ''

lambda_handler()