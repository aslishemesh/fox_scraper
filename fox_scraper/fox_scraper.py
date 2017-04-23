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
        self.main_categories_dict = {}  # contains { Main_category_name: Main_category_link }
        self.sub_categories_dict = {}   # contains { "Sub-Category-Name": sub_category_name,
                                        #            "Sub-Category-Link": sub-category-link }

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
        self.get_main_categories()
        catalog = []
        for main_category in self.main_categories_dict:
            self.get_sub_categories(main_category)
            category_catalog = self.get_category_catalog(main_category)
            catalog.append(category_catalog)
        self.send_all_items(catalog)

    def get_main_categories(self):
        """
        this function will scrap all main catalog categories
        this function will scrap all main catalog categories
        :return: a list of beutifulSoup objects
        """
        main_categories_content = self.get_parsed_web_content(self.site_address)
        main_categories_links = []
        main_categories_scraper = main_categories_content.find_all(class_='link padding_hf_v ')
        for link in main_categories_scraper:
            main_category_name = link.get_text().strip()
            main_category_link = link.get('href')
            main_categories_links.append(main_category_link)
            self.main_categories_dict.update({main_category_name: main_category_link})

    def get_sub_categories(self, main_category):
        """
        this function will scrap sub-catalog links per category
        :param main_category: category link from the site
        :return: a list of sub-categories link per main-category
        """
        category_link = self.main_categories_dict[main_category]
        sub_categories_content = self.get_parsed_web_content(category_link)
        sub_categories = []
        sub_categories_scraper = sub_categories_content.find_all('option')
        for sub_category in sub_categories_scraper:
            current_sub_category = sub_category.get_text().strip()
            current_sub_category = self.verify_item_encoding(current_sub_category)
            sub_categories.append({"Sub-Category-Name": current_sub_category, "Sub-Category-Link": format(sub_category['value'])})
        self.sub_categories_dict.update({main_category: sub_categories})

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

    def get_category_catalog(self, main_category):
        """
        this function will scrap the catalog from a specific category
        :param main_category: main category name
        :return: list of items for this category
        """
        items = []
        for sub_category in self.sub_categories_dict[main_category]:
            sub_category_parser = self.get_parsed_web_content(sub_category["Sub-Category-Link"])
            items += self.get_sub_category_catalog(sub_category_parser, main_category, sub_category["Sub-Category-Name"])
        return items

    def get_sub_category_catalog(self, cat_sub_category, main_category, sub_category):
        """
        this function will receive web content for fox item and returns a list of items
        :param main_category: main category name
        :param sub_category: sub-category main category name
        :param cat_sub_category: web content for fox item
        :return: list of sub-catalog items
        """
        items = []
        sub_category_items_links = cat_sub_category.find_all(
                class_='box padding_hf sp_p_padding_hf center border_b border_l margin_b_1')
        for link in sub_category_items_links:
            current_item = self.parse_item(link, main_category, sub_category)
            items.append(current_item)

        return items

    def parse_item(self, html_item, main_category, sub_category):
        """
        parse the information into Item class
        :return: Item class
        """
        item_img_id = html_item.find_next().get('href')
        item_name = html_item.find_next(class_='pname margin_hf_b').get_text()
        item_price = html_item.find_next(class_='price display_inline numbers').find_next(
            class_='display_inline').get_text()
        nums = item_price.split()
        item_price = float(float(nums[0]) + (float(nums[1])) / 100)
        item = FoxItem(item_img_id, main_category, sub_category,
                       item_name, item_price)
        return item

    def send_all_items(self, catalog):
        """
        send all catalog to rabbitmq
        :param catalog: list of FoxItem's lists
        :return:
        """
        with FoxSender() as rabbit_sender:
            [rabbit_sender.send_message(item) for items in catalog for item in items]
