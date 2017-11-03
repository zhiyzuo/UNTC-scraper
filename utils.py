__author__ = 'Zhiya Zuo'
__email__ = 'zhiyazuo@gmail.com'

import pandas as pd
from bs4 import BeautifulSoup as Soup

BASE_URL = 'https://treaties.un.org'

def parse_tr_list(tr_list):
    l = list()
    for tr in tr_list:
        try:
            if tr['align'] == 'left' and tr['valign'] == 'top':
                l.append(tr)
        except:
            continue
    return pd.DataFrame([parse_tr(tr) for tr in l],
                        columns = ('title', 'link', 'reg_number', 'reg_date', 'tr_type', 'date_conclusion', 'vol'))

def parse_tr(tr):
    td_list = tr.find_all('td')
    l = list()
    for i, td in enumerate(td_list):
        l.append(td.text.strip())
        if i == 0:
            l.append(BASE_URL + td.a['href'])
    return l


if __name__ == '__main__':
    s = '''<tr align="left" class="trBGGrey" valign="top">
<td align="left" valign="top">
<a href="/Pages/showDetails.aspx?objid=080000028000e9b3&amp;clang=_en" id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgTreaty_ctl04_lnktitle" target="_blank" title="Regulation No. 68.  Uniform provisions concerning the approval of power-driven vehicles including pure electric vehicles with regard to the measurement of the maximum speed">Regulation No. 68.  Uniform provisions concerning the approval of power-driven vehicles including pure electr...</a>
</td><td align="left" valign="top">
<span id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgTreaty_ctl04_lbl_RegNo">A-4789</span>
</td><td align="left" valign="top">
<span id="ctl00_ctl00_ContentPlaceHolder1_ContentPlaceHolderInnerPage_dgTreaty_ctl04_lbl_RegDt">01/05/1987</span>
</td><td align="left" valign="top">
                                    Open Multilateral
                                </td><td align="left" valign="top">
                                    01/05/1987
                                </td><td align="left" valign="top">
                                     1462
                                </td>
</tr>'''

    s = Soup(s, 'lxml')

    print parse_tr(s)

