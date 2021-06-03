

import webbrowser

from .models import *
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import  os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select

import time

def main():

    prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs",prefs)
    chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--headless")
    #chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)



    driver.get("https://partner.engineer.ai/login")
    driver.implicitly_wait(20)
    driver.maximize_window()

    user_name='/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/div[1]/input'
    password='/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/div[2]/input'
    submit_button='/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/button'
    billing_button='/html/body/app/div/div[4]/main/core/div/left-menu/div/ul/li[3]'
    no_thanks_button='//*[@id="onesignal-slidedown-cancel-button"]'
    tracked_hours_section='/html/body/app/div/div[4]/main/core/div/div/div/billing/ul/li[3]'
    dates_selection = '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select'

    #on_login_page
    driver.find_element_by_xpath(user_name).send_keys('contact@gemstack.in')  #login_id
    driver.find_element_by_xpath(password).send_keys('contact.gemstack')    #password
    driver.find_element_by_xpath(submit_button).click()


    #choosing billing from left menu
    driver.implicitly_wait(20)
    driver.find_element_by_xpath(billing_button).click()

    '''
    #to_remove the popup
    no_thanks_element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, no_thanks_button)))
    no_thanks_element.click()
    '''

    #to get active elements
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    a=soup.select('li.active')
    print("print statement", a)
    '''

    #try
    '''
    print("in")
    
    
    print("out")
    '''
    driver.implicitly_wait(120)
    '''elem = driver.switch_to_active_element()'''
    driver.find_element_by_xpath(tracked_hours_section).click()


    #/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[1]



    soup = BeautifulSoup(driver.page_source, 'lxml')

    table = soup.find('div',attrs = {'class':'listing-table'})

    # columns = table.find('div',attrs = {'class':'tHead'})
    # columns = columns.findAll('div')
    # for i in columns:
    #     print(i.text)

    # driver.implicitly_wait(120)
    # tdata= soup.find('div',attrs = {'class':'tBody'})
    # tdata

    # records = tdata.findAll('div',attrs = {'class':'tr'})
    # len(records)

    #tdata

    cols = driver.find_element_by_xpath('/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[1]').text
    cols = cols.split('\n')
    print(cols)

    time.sleep(3)
    rows = driver.find_element_by_xpath('/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[2]').text
    rows = rows.split('\n')
    #print(rows)

    import numpy as np
    arr = np.reshape(rows,(int(len(rows)/4),4))

    billing_cycles = driver.find_element_by_xpath('/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select').text
    billing_cycles = billing_cycles.split('\n')
    # print(billing_cycles)

    arr=[]
    for i in range(1,len(billing_cycles)+1):
        driver.find_element_by_xpath(dates_selection+'/option['+str(i)+']').click()
        time.sleep(3)
        rows = driver.find_element_by_xpath('/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[2]').text
        rows = rows.split('\n')
        rows = np.reshape(rows,(int(len(rows)/4),4))
        rows = rows.tolist()
        for j in rows:
            j.append(str(billing_cycles[i-1]))
        arr = arr + rows

    # print(arr)



    for data in arr:

        project_object = Project.objects.create(developer_name=data[0], developer_email=data[1],projects_name=data[2],project_hours=data[3], Month_Cycle=data[4])
        project_object.save()


