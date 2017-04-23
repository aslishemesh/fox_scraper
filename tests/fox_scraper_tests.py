from nose.tools import *
from fox_scraper import Scraper
from fox_scraper import FoxItem
from bs4 import BeautifulSoup
from tests.items_src import catalog


def test_scraper_initialization():
    scrap = Scraper("https://www.fox.co.il/en")
    assert_equal(scrap.site_address, "https://www.fox.co.il/en")


def test_get_categories():
    scrap = Scraper("https://www.fox.co.il/en")
    scrap.get_main_categories()
    main_categories_links = scrap.main_categories_dict
    assert_equal(main_categories_links,
                 {'BABY': u'https://www.fox.co.il/en/BABY',
                  'KIDS': u'https://www.fox.co.il/en/KIDS',
                  'MEN': u'https://www.fox.co.il/en/men',
                  'International': u'https://www.fox.co.il/en/international_2141146',
                  'WOMEN': u'https://www.fox.co.il/en/WOMEN'})


def test_get_sub_categories():
    scrap = Scraper("https://www.fox.co.il/en")
    scrap.get_main_categories()
    scrap.get_sub_categories("WOMEN")
    assert_equal(scrap.sub_categories_dict, {'WOMEN': [
        {"Sub-Category-Name": u'Shirts Woven/Denim',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143357/4143390'},
        {'Sub-Category-Name': u'Shirts Knits',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143357/4143358'},
        {'Sub-Category-Name': u'Tank Tops',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143383'},
        {'Sub-Category-Name': u'Dresses',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143456'},
        {'Sub-Category-Name': u'Pants Shorts',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143406/4143411'},
        {'Sub-Category-Name': u'Pants Tights',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143406/4143409'},
        {'Sub-Category-Name': u'Pants Long',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143406/4143407'},
        {'Sub-Category-Name': u'Skirts',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143449'},
        {'Sub-Category-Name': u'Swimwear',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143350'},
        {'Sub-Category-Name': u'Accessories',
         'Sub-Category-Link': u'https://www.fox.co.il/en/WOMEN/4143343'}]})


def test_get_catalog_sub_category():
    scrap = Scraper("https://www.fox.co.il/en")
    scrap.get_main_categories()
    scrap.get_sub_categories("WOMEN")
    sub_category_catalog = BeautifulSoup(str(catalog), 'html.parser')
    sub_catalog = scrap.get_sub_category_catalog(sub_category_catalog, "WOMEN", "Shirts Woven/Denim")
    items = [FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143405",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143404",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 81.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143403",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 129.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143402",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143397",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143393",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 79.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143391",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143474",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 129.9),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143477",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9)]

    assert_equal(sub_catalog, items)


def test_send_item():
    scrap = Scraper("https://www.fox.co.il/en")

    items = [[FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143405",
                      "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 119.9),
              FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143404",
                      "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", 81.9)],
             [FoxItem("https://www.fox.co.il/en/MEN/4143357/4143390/4143474",
                      "MEN", "Shirts Woven/Denim", "T-SHIRT", 100.9),
              FoxItem("https://www.fox.co.il/en/MEN/4143357/4143390/4143477",
                      "MEN", "Shirts Woven/Denim", "T-SHIRT", 70.9)]]

    scrap.send_all_items(items)
