from fetch_data import billing_cycles, arr
import time
import webbrowser
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
chrome_options = Options()
import time


prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
chrome_options.add_experimental_option("prefs",prefs)
chrome_options.add_argument("--no-sandbox")
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-setuid-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument('--disable-features=VizDisplayCompositor')
driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)


user_name='//*[@id="id_username"]'
password='//*[@id="id_password"]'
submit_button='/html/body/div/form/button'
add_project='/html/body/button[1]'
project_name='//*[@id="id_projects_name"]'
project_hours='//*[@id="id_project_hours"]'
dev_name='//*[@id="id_developer_name"]'
p_time='//*[@id="id_project_time"]'
p_start_date='//*[@id="id_project_start_date"]'
p_end_date='//*[@id="id_project_end_date"]'
email='//*[@id="id_employee_email"]'
submit_button1='/html/body/div/form/button'
dates_selection = '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select'


driver.get("http://localhost:8000")
driver.implicitly_wait(20)
driver.maximize_window()


#on_login_page
driver.find_element_by_xpath(user_name).send_keys('Proton')
driver.find_element_by_xpath(password).send_keys('123456')
driver.find_element_by_xpath(submit_button).click()
driver.find_element_by_xpath(add_project).click()

def main():        
    for i in arr:
        driver.implicitly_wait(20)
    
        split_date=i[4].split(" - ")
        start_date=split_date[0]
        end_date=split_date[1]
        time.sleep(3)
        #name of developer
        driver.find_element_by_xpath(dev_name).send_keys(i[0])
        #email
        driver.find_element_by_xpath(email).send_keys(i[1])
        #name_of_project
        driver.find_element_by_xpath(project_name).send_keys(i[2])
        #hours
        driver.find_element_by_xpath(project_hours).send_keys(i[3])
        driver.implicitly_wait(20)
        # convert in date (TODO)
        driver.find_element_by_xpath(p_start_date).send_keys(start_date)
        driver.find_element_by_xpath(p_end_date).send_keys(end_date)
        driver.implicitly_wait(10)

        driver.find_element_by_xpath(submit_button1).click()
        driver.implicitly_wait(20)
        driver.find_element_by_xpath(add_project).click()


main()

driver.close()
