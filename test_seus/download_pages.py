# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 15:07:01 2020

@author: ars14
"""
import time
from selenium import webdriver
import random
import urllib.request

# получение HTML кода 
driver = webdriver.Chrome("C:\chromedriver")
driver.get("http://unro.minjust.ru/NKOReports.aspx?request_type=inko")
time.sleep(3)
Vid = driver.find_element_by_css_selector("#filter_nko_form :nth-child(2)")
time.sleep(3)
Vid.click()
time.sleep(3)
dt_from = driver.find_element_by_css_selector("#filter_dt_from :nth-child(2)")
dt_from.click()
time.sleep(3)
btn = driver.find_element_by_css_selector("#b_refresh")
btn.click()
time.sleep(3)
pdg = driver.find_element_by_css_selector(".pdg_count:last-child")
pdg.click()
time.sleep(3)
main_page1 = driver.page_source
btn_next = driver.find_element_by_css_selector("#pdg_next")
btn_next.click()
main_page2 = driver.page_source
time.sleep(3)
driver.quit()

# выделение нужных ID документов
id_index = [i for i in range(len(main_page1)) if main_page1.startswith('pk=', i)]
id_index2 = [i for i in range(len(main_page2)) if main_page2.startswith('pk=', i)]
IDs = []
for id_ind in id_index:
    IDs.append(str(main_page1[(id_ind+4):(id_ind+12)]))
for id_ind2 in id_index2:
    IDs.append(str(main_page2[(id_ind2+4):(id_ind2+12)]))

# cкачивание файлов
prox = ['88.198.24.108', '138.68.41.90', '191.96.42.80', '198.199.86.11']
err_ex_list = []
err_ex_list2 = []
exep = []
for i in IDs:
    try:
        page_link = 'http://unro.minjust.ru/Reports/'+str(i)+'.pdf'
        a = random.choice(prox)
        a_new = 'http://'+a+':8080'
        proxies = {'http' : a}
        down_link = './отчёты/'+a+'/'+str(i)+'.pdf'
        urllib.request.urlretrieve(page_link, down_link)
    except Exception:
        err_ex_list.append(i)
# вторая попытка
for i in err_ex_list:
    try:
        page_link = 'http://unro.minjust.ru/Reports/'+str(i)+'.pdf'
        a = random.choice(prox)
        a_new = 'http://'+a+':8080'
        proxies = {'http' : a}
        down_link = './отчёты/'+a+'/'+str(i)+'.pdf'
        urllib.request.urlretrieve(page_link, down_link)
    except Exception as ex:
        err_ex_list2.append(i) #запись id отчётов с ошибками
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        exep.append(message)

with open('listfile.txt', 'w') as filehandle:  
    filehandle.writelines("%s\n" % item for item in err_ex_list2)






















