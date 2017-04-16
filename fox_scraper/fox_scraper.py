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
            1. runner() - this will be the main function for the site scraping it will retrieve
               the main categories (women, men, kids, baby) and use helper functions for retrieving other categories and cloths
            2. publish_data_to_rabbitmq() - this function will publish all data towards rabbitmq
'''


from bs4 import BeautifulSoup
from fox_helper import FoxItem
from fox_helper import FoxSender
import requests


class Scraper:
    def __init__(self, site_address):
        self.site_address = site_address
        self.main_categories = []
        self.sub_categories = []

    def get_parsed_web_content(self, http_address):
        """
        :param http_address: url address to send a request
        :return: an html parse text to be scrap from (beutifulsoup object)
        """
        raw_data = requests.get(http_address)
        return BeautifulSoup(raw_data.text, 'html.parser')

    def runner(self):
        """
        one of the main function for this class.
        this function will activate the scraping of the web address revieced on contruction of the class
        :return: a list of items (Item class) of the entire catalog
        """
        main_categories_links = self.get_main_categories()
        catalog = []
        for main_cat_num in range(len(main_categories_links)):
            sub_categories = self.get_sub_categories(main_categories_links[main_cat_num], main_cat_num)
            category_catalog = self.get_category_catalog(sub_categories, main_cat_num)
            catalog.append(category_catalog)
        return catalog

    def get_main_categories(self):
        """
        this function will scrap all main catalog categories
        :return: a list of beutifulSoup objects
        """
        main_categories_content = self.get_parsed_web_content(self.site_address)
        main_categories_links = []
        for link in main_categories_content.find_all(class_='link padding_hf_v '):
            main_categories_links.append(link.get('href'))
            self.main_categories.append(link.get_text().strip())
        return main_categories_links

    def get_sub_categories(self, category_link, category_num):
        """
        this function will scrap sub-catalog links per category
        :param category_link: sub-category link from the site
        :param category_num: category number for item description
        :return: a list of sub-categories link per main-category
        """
        sub_categories_content = self.get_parsed_web_content(str(category_link))
        sub_categories = []
        self.sub_categories.append([])
        for sub_category in sub_categories_content.find_all('option'):
            current_sub_category = self.verify_item_encoding((sub_category.get_text()).strip())
            self.sub_categories[category_num].append(current_sub_category)
            sub_categories.append(format(sub_category['value']))
        return sub_categories

    def verify_item_encoding(self, item_name):
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

    def get_category_catalog(self, sub_categories, main_cat_num):
        """
        this function will scrap the catalog from a specific category
        :param sub_categories: beutifulSoup object of a specific category
        :param main_cat_num: main category number
        :return: list of items for this category
        """
        items = []
        for sub_cat_num in range(len(sub_categories)):
            cat_sub_category = self.get_parsed_web_content(sub_categories[sub_cat_num])
            items += self.get_sub_category_catalog(cat_sub_category, main_cat_num, sub_cat_num)
        return items

    def get_sub_category_catalog(self, cat_sub_category, main_cat_num, sub_cat_num):
        """
        this function will receive web content for fox item and returns a list of items
        :param cat_sub_category: web content for fox item
        :param main_cat_num: main category number
        :return:
        """
        items = []
        for link in cat_sub_category.find_all(class_='box padding_hf sp_p_padding_hf center border_b border_l margin_b_1'):
            items.append(self.parse_item(link, main_cat_num, sub_cat_num))

        return items

    def parse_item(self, html_item, main_cat_num, sub_cat_num):
        """
        parse the information into Item class
        :return: Item class
        """
        item_img_id = html_item.find_next().get('href')
        item_name = html_item.find_next(class_='pname margin_hf_b').get_text()
        item_price = html_item.find_next(class_='price display_inline numbers').find_next(class_='display_inline').get_text()
        nums = item_price.split()
        item_price = float(float(nums[0]) + (float(nums[1])) / 100)
        item = FoxItem(item_img_id, self.main_categories[main_cat_num], self.sub_categories[main_cat_num][sub_cat_num], item_name, item_price)
        return item


    # TODO - change location to new "program" function and not here
    def send_all_items(self, catalog):

        rabbit_sender = FoxSender()
        for items in catalog:
            for item in items:
                rabbit_sender.send_message(item)
        rabbit_sender.close_connection()

# Temp test for debugging...
"""
print "start"
item = FoxItem("1","2","3","4",5)
print item.__dict__
scrap = Scraper("https://www.fox.co.il/en")
scrap.send_all_items(scrap.runner())
"""