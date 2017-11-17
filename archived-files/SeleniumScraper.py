import time

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as Soup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Scraper(object):
    def __init__(self):
        url = 'https://treaties.un.org/Pages/AdvanceSearch.aspx?tab=UNTS&clang=_en'
        self.browser = webdriver.Chrome()
        self.browser.get(url)
        self.base_url = 'https://treaties.un.org'
        #time.sleep(np.random.randint(7, 10))

        self.column_names = ['href', 'title', 'reg_num', 'reg_date', 'type', 'con_date', 'vol']
        self.df = pd.DataFrame(columns=self.column_names)
        self.tid = 'ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgTreaty'

        self._set_criteria()


    def _set_criteria(self):
        ## Search for Treaty
        select = Select(self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpSearchObj'))
        select.select_by_visible_text('Treaty')
        time.sleep(np.random.randint(1,2))
        ## Select Show Only Original Agreement
        self.browser.find_element_by_id('ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_rdbtreaty_2').send_keys(Keys.SPACE)
        #time.sleep(np.random.randint(10, 15))

        ## Select filter by: Treaty type
        select = Select(self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute'))
        time.sleep(np.random.randint(1,2))
        ## the 20th one is `Treaty type`
        select.select_by_index(20)
        ## Select "Open Multilateral"
        self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$chkboxValues$2').send_keys(Keys.SPACE)
        #time.sleep(np.random.randint(10, 15))
        time.sleep(np.random.randint(1,2))
        self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$Adv_srch2').send_keys(Keys.SPACE)

        self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnAdd').send_keys(Keys.SPACE)

    def set_year(self, from_date, to_date):
        if '3' in from_date:
            from_date = from_date.replace('3', Keys.NUMPAD3)
        if '3' in to_date:
            to_date = to_date.replace('3', Keys.NUMPAD3)
        select = Select(self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute'))
        select.select_by_visible_text('Date of Registration')
        from_field = self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$txtFrom')
        from_field.click()
        from_field.clear()
        from_field.send_keys(from_date)
        to_field = self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$txtTo')
        to_field.click()
        to_field.clear()
        to_field.send_keys(to_date)

        #time.sleep(np.random.randint(10, 15))
        self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnAdd').send_keys(Keys.SPACE)

    def search(self):
        time.sleep(np.random.randint(2, 5))
        self.browser.find_element_by_name('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnSubmit').send_keys(Keys.SPACE)
        self._iterate()


    def _iterate(self):
        while True:
            tbody = self.browser.find_element_by_id(self.tid).find_element_by_tag_name('tbody')
            tr_list = tbody.find_elements_by_tag_name('tr')
            self.df = self.df.append(self.parse_page(tr_list[3:-2]), ignore_index=True)
	    print self.df
            #btn = WebDriverWait(self.browser, np.random.randint(2, 5)).until(_find)
            d = len(tr_list)
            #id_ = 'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$dgTreaty$ctl01$ctl%d'%(d)
            #print id_
            #btn = WebDriverWait(self.browser,
            #                    np.random.randint(5,7)).until(EC.presence_of_element_located((By.NAME, id_)))

            if btn.get_attribute('disabled') is not None:
                break

            print 'Now have %d rows'%(self.df.shape[0])

            #btn = WebDriverWait(self.browser, np.random.randint(2, 5)).until(_find)
            #btn.send_keys(Keys.SPACE)

    def parse_page(self, tr_list):
	tmp = list()
	for tr in tr_list:
	    tmp.append(list())
	    for i, td in enumerate(tr.find_elements_by_tag_name('td')):
		if i == 0:
		    tmp[-1].append(td.find_element_by_tag_name('a').get_attribute('href'))
        return pd.DataFrame(tmp, columns=self.column_names)

    def close(self):
        self.browser.close()
