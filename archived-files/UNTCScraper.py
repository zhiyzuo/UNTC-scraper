__author__ = 'Zhiya Zuo'
__email__ = 'zhiyazuo@gmail.com'

import time
import random
import warnings
import mechanize
import pandas as pd
from utils import parse_tr_list
from bs4 import BeautifulSoup as Soup

class UNTCScraper(object):
    def __init__(self, endpage=None):
        self.url = "https://treaties.un.org/Pages/AdvanceSearch.aspx?tab=UNTS&clang=_en"
        self.endpage = endpage

        self.br = mechanize.Browser()
        self.br.addheaders = [('User-agent',
                               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.63 Safari/535.7')]

        self.br.open(self.url)
        self.br.select_form('aspnetForm')

        ctl = self.br.form.find_control('__EVENTTARGET')
        ctl.readonly = False
        ## select "Show only original agreement"
        self.br.form['__EVENTTARGET'] = 'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$dgTreaty$2'
        ctl.readonly = True

        ctl = self.br.form.find_control('__EVENTARGUMENT')
        ctl.readonly = False
        pageno = 1
        self.br.form['__EVENTARGUMENT'] = 'Page$%d'%pageno
        ctl.readonly = True

        self.br.form['ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpSearchObj'] = ['ts_treaty']

        ctl = self.br.form.find_control("ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnSubmit")
        ctl.disabled = False

    def set_treaty_type(self, ):
        #print self.br.form['ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute']
        ctl = self.br.form.find_control('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$drpAttribute')
        ctl.readonly = False
        # ['treaty_type_indicator']
        #print self.br.form['ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_chkboxValues']
        #open_multi = 'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$chkboxValues'
        #self.br.form.find_control(open_multi).get(open_multi+'$2').selected = True

    def set_endpage(self, endpage):
        self.endpage = endpage

    def _parse(self, content):
        table = content.find('table')
        tr_thead = table.find('tr', class_='thead-one')
        return tr_thead.find_all_next('tr')

    def scrape(self):
        if self.endpage is None:
            warnings.warn("Please set endpage first using `UNTCScrapper.set_endpage(endpage)` method!")
            return
        if self.endpage < 2:
            warnings.warn("`endpage` needs to be > 2!")
            return

        resp = self.br.submit('ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$btnSubmit')
        content = Soup(self.br.response().read(), 'lxml')

        self.df = parse_tr_list(self._parse(content))

        for pageno in range(2, self.endpage+1):
            ## sleep < 10s
            time.sleep(random.random()*10)
            self.df = self.df.append(parse_tr_list(self.scrape_page(pageno)), ignore_index=True)

    def scrape_page(self, pageno):
        self.br.select_form('aspnetForm')
        ctl = self.br.form.find_control('__EVENTTARGET')
        ctl.readonly = False
        self.br.form['__EVENTTARGET'] = 'ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolderInnerPage$dgTreaty'
        ctl.readonly = True

        ctl = self.br.form.find_control('__EVENTARGUMENT')
        ctl.readonly = False
        self.br.form['__EVENTARGUMENT'] = 'Page$%d'%pageno
        ctl.readonly = True

        self.br.submit()
        content = Soup(self.br.response().read(), 'lxml')
        return self._parse(content)

