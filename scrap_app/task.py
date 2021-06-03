from celery.task.schedules import crontab
from celery.decorators import periodic_task
from scrap_app.user_addition import add_user
from .utils import main_function,send_emails
from .models import Project
# from .fetch_data import billing_cycles, arr
# import time
# import webbrowser
# from bs4 import BeautifulSoup, NavigableString, Tag 
# from selenium.webdriver.chrome.options import Options
# from selenium import webdriver
# import os
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import sys
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.support.select import Select
import time



@periodic_task(run_every=(crontab(hours='0',minute='0',day_of_week='mon-fri')), name="some_task", ignore_result=True)
def task_employe_worker():
	workers = []
	worker = Project.objects.all()
	for work_time in worker:
		if work_time.project_working_hrs is None:
			time_input = work_time.project_hours
		else:
			time_input = work_time.project_working_hrs
		time_left = work_time.project_left_hrs
		workers.append(main_function(time_input,time_left,1))
		for work in workers:
			work_time.project_working_hrs=work
			work_time.save()


# @periodic_task(run_every=(crontab(minute='30',hours='0',day_of_week='mon-fri')), name="project_data", ignore_result=True)
# def some_task():
# 	chrome_options = Options()
# 	prefs = {"profile.default_content_setting_values.notifications" : 2}  #block notifications
# 	chrome_options.add_experimental_option("prefs",prefs)
# 	chrome_options.add_argument("--no-sandbox")
# 	chrome_options.add_argument("--headless")
# 	#chrome_options.add_argument("--disable-setuid-sandbox")
# 	chrome_options.add_argument("--disable-dev-shm-usage")
# 	#chrome_options.add_argument('--disable-features=VizDisplayCompositor')
# 	driver = webdriver.Chrome(ChromeDriverManager().install(),options=chrome_options)


# 	user_name='//*[@id="id_username"]'
# 	password='//*[@id="id_password"]'
# 	submit_button='/html/body/div/form/button'
# 	add_project='/html/body/button[1]'
# 	project_name='//*[@id="id_projects_name"]'
# 	project_hours='//*[@id="id_project_hours"]'
# 	dev_name='//*[@id="id_developer_name"]'
# 	p_time='//*[@id="id_project_time"]'
# 	p_start_date='//*[@id="id_project_start_date"]'
# 	p_end_date='//*[@id="id_project_end_date"]'
# 	submit_button1='/html/body/div/form/button'
# 	dates_selection = '/html/body/app/div/div[4]/main/core/div/div/div/billing/app-tracked-hours/div[1]/div[1]/select'
# 	email='//*[@id="id_employee_email"]'

# 	driver.get("http://127.0.0.1:8000/")
# 	driver.implicitly_wait(20)
# 	driver.maximize_window()


# 	#on_login_page
# 	driver.find_element_by_xpath(user_name).send_keys('Proton')
# 	driver.find_element_by_xpath(password).send_keys('123456')
# 	driver.find_element_by_xpath(submit_button).click()
# 	driver.find_element_by_xpath(add_project).click()


# 	def main():        
# 		for i in arr:
# 			driver.implicitly_wait(20)

# 			split_date=i[4].split(" - ")
# 			start_date=split_date[0]
# 			end_date=split_date[1]
# 			time.sleep(3)
# 			#name of developer
# 			driver.find_element_by_xpath(dev_name).send_keys(i[0])

# 			#email
# 			driver.find_element_by_xpath(email).send_keys(i[1])

# 			#name_of_project
# 			driver.find_element_by_xpath(project_name).send_keys(i[2])
# 			#hours
# 			driver.find_element_by_xpath(project_hours).send_keys(i[3])

# 			#driver.find_element_by_xpath(Project_working_hrs).send_keys(i[3])
# 			driver.implicitly_wait(20)
# 			driver.find_element_by_xpath(p_start_date).send_keys(start_date)
# 			driver.find_element_by_xpath(p_end_date).send_keys(end_date)
# 			driver.implicitly_wait(10)



# 			driver.find_element_by_xpath(submit_button1).click()
# 			driver.implicitly_wait(20)
# 			driver.find_element_by_xpath(add_project).click()
# 		main()

# 	driver.close()



@periodic_task(run_every=(crontab(minute='40',hours='0',day_of_week='mon-fri')), name="some_task", ignore_result=True)
def task_email():
	workers = []
	worker = Project.objects.all()
	for work_time in worker:
		time_input = work_time.project_working_hrs
		time_left = work_time.project_hours
		workers.append(main_function(time_input,time_left,0))
		for work in workers:
			work_time.mailing_hrs=str(work)
			work_time.save()
			send_emails(user_name=work_time.developer_name,pending_hrs=work_time.mailing_hrs,email=work_time.employee_email,project_name=work_time.projects_name)
		print("Mails sent to users")
