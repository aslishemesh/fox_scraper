# coding=utf-8

'''
1. Scraper overview:
    1. Scrap all clothes catalog from Fox site
    2. Publish all data to rabbitmq:
        1. Exchange name - “fox_scrap”
        2. Exchange type - “direct”
        3. routing_key - “fox”
    3. The scraper will retrieve site’s information (“requests” package)
    4. The scraper will scrap the requested data (“bs4” package - BeautifulSoup)
    5. The scraper will send the data to rabbitmq (“pika” package)
    6. Scraper structure:
        1. The scraper input - a site address link
        2. The scraper output - all Fox’s catalog
        3. The scraper will use two main functions:
            1. scrap_fox_runner() - this will be the main function for the site scraping it will retrieve
               the main categories (women, men, kids, baby) and use helper functions for retrieving other categories and cloths
            2. publish_data_to_rabbitmq() - this function will publish all data towards rabbitmq
'''


from bs4 import BeautifulSoup
import requests

class fox_item(object):
    def __init__(self, item_img_id, item_main_category, item_type, item_name, item_price):
        self.item_img_id = item_img_id
        self.item_main_category = item_main_category
        self.item_type = item_type
        self.item_name = item_name
        self.item_price = item_price

    def print_item(self):
        print "item image id:", self.item_img_id
        print "item main category:", self.item_main_category
        print "item type:", self.item_type
        print "item name:", self.item_name
        print "item price: %.2f " %self.item_price


class Scraper:
    def __init__(self, site_address):
        self.site_address = site_address
        self.main_categories = []
        self.sub_categories = []

    def get_web_content(self, http_address):
        """
        :param http_address: url address to send a request
        :return: an html text to be scrap from
        """
        raw_data = requests.get(http_address)
        return raw_data.text

    def get_soup_object(self, web_text):
        """
        :param web_text: html txt file to scrap
        :return: beautiful soup objet for scraping
        """
        return BeautifulSoup(web_text, 'html.parser')

    def scrap_fox_runner(self):
        """
        one of the main function for this class.
        this function will activate the scraping of the web address revieced on contruction of the class
        :return: a list of items (Item class) of the entire catalog
        """
        soup_main_categories = self.scrap_fox_main_categories()
        catalog = []
        soup_sub_categories = []
        main_cat_num = 0
        for soup_main_category in soup_main_categories:
            soup_sub_categories += list(self.scrap_fox_sub_categories(soup_main_category, main_cat_num))
            catalog.append(self.scrap_fox_catalog(soup_sub_categories, main_cat_num))
            main_cat_num += 1
        return catalog

    def scrap_fox_main_categories(self):
        """
        this function will scrap all main catalog categories
        :return: a list of beutifulSoup objects
        """
        soup_main_category = self.get_soup_object(self.get_web_content(self.site_address))
        main_categories = []
        for link in soup_main_category.find_all(class_='link padding_hf_v '):
            main_categories.append(link.get('href'))
            self.main_categories.append(link.get_text().strip())
        return main_categories

    def scrap_fox_sub_categories(self, soup_category, category_num):
        """
        this function will scrap all catalog per sub category
        :param soup_category: sub-category link from the site
        :param category_num: category number for item description
        :return: a list of catalog items per sub-category
        """
        sub_categories = self.get_soup_object(self.get_web_content(str(soup_category)))
        sub_catalog = []
        self.sub_categories.append(category_num)
        self.sub_categories[category_num] = []
        for sub_category in sub_categories.find_all('option'):
            self.sub_categories[category_num].append(self.verify_encoding((sub_category.get_text()).strip()))
            sub_catalog.append(format(sub_category['value']))
        return sub_catalog

    def verify_encoding(self, item_name):
        """
        overcome encoding problem using split
        :param item_name: string of sub-category
        :return: string of sub-category without encoding problem
        """
        list1 = item_name.split()
        if len(list1) > 1:
            return list1[0] + " " + list1[-1]
        else:
            return item_name

    def scrap_fox_catalog(self, soup_sub_categories, main_cat_num):
        """
        this function will scrap the catalog from a specific category
        :param soup_sub_categories: beutifulSoup object of a specific category
        :param main_cat_num: main category number
        :return: list of items for this category
        """
        items = []
        for soup_sub_category in soup_sub_categories:
            soup_cat_sub_category = self.get_soup_object(self.get_web_content(soup_sub_category))
            sub_cat_num = 0
            for link in soup_cat_sub_category.find_all(class_='box padding_hf sp_p_padding_hf center border_b border_l margin_b_1'):
                items.append(self.parse_item(link, main_cat_num, sub_cat_num))
            sub_cat_num += 1
        return items

    def parse_item(self, soup_item, main_cat_num, sub_cat_num):
        """
        parse the information into Item class
        :return: Item class
        """
        item_img_id = soup_item.find_next().get('href')
        item_name = soup_item.find_next(class_='pname margin_hf_b').get_text()
        item_price = soup_item.find_next(class_='price display_inline numbers').find_next(class_='display_inline').get_text()
        nums = item_price.split()
        item_price = float(float(nums[0]) + (float(nums[1])) / 100)
        item = fox_item(item_img_id, self.main_categories[main_cat_num], self.sub_categories[main_cat_num][sub_cat_num], item_name, item_price)
        return item

print "start"
scrap = Scraper("https://www.fox.co.il/en")
print scrap.scrap_fox_runner()
