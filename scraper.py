# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 20:27:50 2023

@author: RDxR10
"""

import time
from selenium import webdriver
import csv
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

query = input("Enter job query: ")
location = input("Enter job location: ")
num_pages = int(input("Number of pages: "))
start_list = [page * 10 for page in range(num_pages)]
base_url = 'https://in.indeed.com'
#base_url = "https://www.indeed.com'

driver = webdriver.Chrome(ChromeDriverManager().install())

for start in start_list:
    url = base_url + f'/jobs?q={query}&l={location}&start={start}'
    driver.execute_script(f"window.open('{url}', 'tab{start}');")
    time.sleep(1)

with open(f'{query}_{location}_job_results.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Job Title', 'Company', 'Location', 'Job Link', 'Salary'])
    for start in start_list:
        driver.switch_to.window(f'tab{start}')

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('td', {'class': 'resultContent'})

        for job in items:
            s_link = job.find('a').get('href')
            job_title = job.find('span', title=True).text.strip()
            company = job.find('span', class_='companyName').text.strip()
            location = job.find('div', class_='companyLocation').text.strip()
            if job.find('div', class_='metadata salary-snippet-container'):
                salary = job.find('div', class_='metadata salary-snippet-container').text
            elif job.find('div', class_='metadata estimated-salary-container'):
                salary = job.find('div', class_='metadata estimated-salary-container').text
            else:
                salary = ""

            job_link = base_url + s_link

            writer.writerow([job_title, company, location, job_link, salary])

        driver.close()


driver.quit()
