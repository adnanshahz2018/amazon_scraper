
import json, threading
from bs4 import BeautifulSoup
from selenium import webdriver 

audible_best_sellers    = 'https://www.amazon.com/Best-Sellers-Audible-Audiobooks/zgbs/audible/?_encoding=UTF8&ref_=sv_adbl_subnav_ref1_2'
kindle_best_sellers     = 'https://www.amazon.com/Best-Sellers-Kindle-Store-eBooks/zgbs/digital-text/154606011/ref=zg_bs_nav_kstore_1_kstore'
audible_categories_us   = {}
kindle_categories_us    = {}


class audible:
    count = 0
    browser = None

    def category(self):
        self.browser = webdriver.Chrome('chromedriver.exe') 
        self.browser.get(audible_best_sellers)
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        ul = soup.find('ul', attrs={'id':'zg_browseRoot'})
        ul = ul.find('ul')
        our_ul = ul.find('ul')
        li_list = our_ul.find_all('li')
        for li in li_list:
            self.count += 1
            cat = li.get_text()
            link = li.find('a')['href']
            audible_categories_us[cat] =  self.check_subcategory(cat, link)
            print('A - ', self.count, '. \n"' + cat + '"', ' : ', audible_categories_us[cat], '\n')
            with open('audible_list.json', 'w+') as jasonfile:
                json.dump(audible_categories_us, jasonfile, indent=4)
        self.browser.close()
        
    def check_subcategory(self, cat, link):
        cat_dict = {}
        self.browser.get(link)
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        li = soup.find('span', attrs={'class':'zg_selected'}).parent
        ul = li.parent
        try:
            our_ul = ul.find('ul')
            cat_dict['null'] = link 
            li_list = our_ul.find_all('li')
            for li in li_list:
                cat = li.get_text()
                link = li.find('a')['href']
                cat_dict[cat] =  self.check_subcategory(cat, link)
        except: return link
        return cat_dict


class kindle:
    count = 0
    browser = None

    def category(self):
        self.browser = webdriver.Chrome('chromedriver.exe') 
        self.browser.get(kindle_best_sellers)
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        ul = soup.find('ul', attrs={'id':'zg_browseRoot'})
        ul = ul.find('ul')
        ul = ul.find('ul')
        our_ul = ul.find('ul')
        li_list = our_ul.find_all('li')
        for li in li_list:
            self.count += 1
            cat = li.get_text()
            link = li.find('a')['href']
            kindle_categories_us[cat] =  self.check_subcategory(cat, link)
            print('K - ', self.count, '. \n"' + cat + '"', ' : ', kindle_categories_us[cat], '\n')
            with open('kindle_list.json', 'w+') as jasonfile:
                json.dump(kindle_categories_us, jasonfile, indent=4)
        self.browser.close()
        
    def check_subcategory(self, cat, link):
        cat_dict = {}
        self.browser.get(link)
        soup = BeautifulSoup(self.browser.page_source, features='lxml')
        li = soup.find('span', attrs={'class':'zg_selected'}).parent
        ul = li.parent
        try:
            our_ul = ul.find('ul')
            cat_dict['null'] = link 
            li_list = our_ul.find_all('li')
            for li in li_list:
                cat = li.get_text()
                link = li.find('a')['href']
                cat_dict[cat] =  self.check_subcategory(cat, link)
        except: return link
        return cat_dict


if __name__ == '__main__':
    audi = audible()
    kind = kindle()
    print('\n')
    threading.Thread(target=audi.category).start()
    threading.Thread(target=kind.category).start()
    