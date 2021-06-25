import webbrowser
from .models import *
from bs4 import BeautifulSoup, NavigableString, Tag
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from dateutil.parser import parse
import re
# import check_hour as ch



import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.select import Select

import time

billing_cycles = []

def get_time(t):
    # import pdb; pdb.set_trace()
    a = re.split(' ', t)
    if (len(a) == 6):
        a = [int(a[0]), int(a[2]), int(a[4])]
    elif (len(a) == 4):
        a = [int(a[0]), int(a[2]), 0]
    elif (len(a) == 2):
        a = [int(a[0]), 0, 0]
    else:
        a = [0, 0, 0]
    return a

def convert(seconds):
    print(seconds)
    a=str(seconds//3600)
    b=str((seconds%3600)//60)
    c=str((seconds%3600)%60)
    return a,b,c


def main():
    global billing_cycles
    # Project.objects.all().delete()
    prefs = {"profile.default_content_setting_values.notifications": 2}  # block notifications
    chrome_options = Options()
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument('--disable-features=VizDisplayCompositor')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get("https://partner.engineer.ai/login")
    driver.implicitly_wait(20)
    driver.maximize_window()

    user_name = '/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/div[1]/input'
    password = '/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/div[2]/input'
    submit_button = '/html/body/app/div/div[4]/main/login/div/div[2]/form/div/div/div/button'
    billing_button = '/html/body/app/div/div[4]/main/core/div/left-menu/div/ul/li[3]'
    no_thanks_button = '//*[@id="onesignal-slidedown-cancel-button"]'
    tracked_hours_section = '/html/body/app/div/div[4]/main/core/div/div/div/billing/ul/li[3]'
    dates_selection = '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select'

    # on_login_page
    driver.find_element_by_xpath(user_name).send_keys('contact@gemstack.in')  # login_id
    driver.find_element_by_xpath(password).send_keys('contact.gemstack')  # password
    driver.find_element_by_xpath(submit_button).click()

    # choosing billing from left menu
    driver.implicitly_wait(20)
    driver.find_element_by_xpath(billing_button).click()

    '''
    #to_remove the popup
    no_thanks_element = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.XPATH, no_thanks_button)))
    no_thanks_element.click()
    '''

    # to get active elements
    '''
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    a=soup.select('li.active')
    print("print statement", a)
    '''

    # try
    '''
    print("in")


    print("out")
    '''
    driver.implicitly_wait(120)
    '''elem = driver.switch_to_active_element()'''
    driver.find_element_by_xpath(tracked_hours_section).click()

    # /html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[1]

    soup = BeautifulSoup(driver.page_source, 'lxml')

    table = soup.find('div', attrs={'class': 'listing-table'})
    cols = driver.find_element_by_xpath(
        '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[1]').text
    cols = cols.split('\n')
    print(cols)
    time.sleep(3)
    rows = driver.find_element_by_xpath(
        '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[2]').text
    rows = rows.split('\n')
    import numpy as np
    # arr = np.reshape(rows, (int(len(rows) / 4), 4))

    billing_cycles = driver.find_element_by_xpath(
        '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select').text
    billing_cycles = billing_cycles.split('\n')
    print(billing_cycles)


    arr = []
    data_in_db = Project.objects.all()

    if data_in_db.exists():
        print("===========================in db=============")
        rows = driver.find_element_by_xpath(
            '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[2]').text
        rows = rows.split('\n')
        rows = np.reshape(rows, (int(len(rows) / 4), 4))
        rows = rows.tolist()
        for j in rows:
            j.append(str(billing_cycles[len(billing_cycles) - 1 - 1]))
        arr = arr + rows

        # print(arr)
        last_cycle = Project.objects.filter(Month_Cycle = billing_cycles[-1] )
        for data,x in zip(last_cycle, arr):
            data.Month_Cycle = x[3]
        

    else:
        print("====================== Not in ========================")
        for i in range(1, len(billing_cycles) + 1):
            driver.find_element_by_xpath(dates_selection + '/option[' + str(i) + ']').click()
            time.sleep(3)
            rows = driver.find_element_by_xpath(
                '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[2]/div[2]').text
            rows = rows.split('\n')
            rows = np.reshape(rows, (int(len(rows) / 4), 4))
            rows = rows.tolist()
            for j in rows:
                j.append(str(billing_cycles[i - 1]))
            arr = arr + rows

        # print(arr)

        for data in arr:
            project_object = Project.objects.create(developer_name=data[0], developer_email=data[1], projects_name=data[2],
                                                    project_hours=data[3], Month_Cycle=data[4])
            project_object.save()

    proj_obj = Project.objects.all()

    for i in proj_obj:
        print("here")
        print(i)

        print(i.project_hours)
        print(i.expected_cycle_hours)

        fetched_hrs = get_time(i.project_hours)
        expected_hours = get_time(i.expected_cycle_hours)
        print(fetched_hrs)
        print(expected_hours)

        # import pdb; pdb.set_trace()
        if(fetched_hrs[0]>expected_hours[0]):
            print("in if")
            i.cycle_hour_diff=0
            i.save()
        else:
            total_sec_f = (fetched_hrs[0] * 60 * 60) + (fetched_hrs[1] * 60) + fetched_hrs[2]
            total_sec_e = (expected_hours[0] * 60 * 60) + (expected_hours[1] * 60) + expected_hours[2]
            sub_hrs_sec = total_sec_e  - total_sec_f
            i.cycle_hour_diff = (sub_hrs_sec)
            i.save()




    driver.close()


def get_expected_hours():
    global billing_cycles
    for i in billing_cycles:
        a = i.split(' - ')
        start = parse(a[0])
        end = parse(a[1])
        print(start, end)
        no_of_days = (end - start).days
        hol = Holidays.objects.filter(holidays__gte=start, holidays__lte=end).count()
        print(hol)
        work_days = no_of_days - hol
        expected_cycle_hours = work_days * 8
        print(expected_cycle_hours)
        billing_cycles_data = Project.objects.filter(Month_Cycle=i)
        billing_cycles_data.update(expected_cycle_hours=(str(expected_cycle_hours) + ' Hr'))






if __name__ == "__main__":
    main()


