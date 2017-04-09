from nose.tools import *
from fox_scraper import Scraper
from fox_scraper import FoxItem
from bs4 import BeautifulSoup
from tests.items_src import catalog

def test_scraper_initialization():
    scrap = Scraper("https://www.fox.co.il/en")
    assert_equal(scrap.site_address, "https://www.fox.co.il/en")
    assert_equal(scrap.main_categories, [])
    assert_equal(scrap.sub_categories, [])


def test_get_categories():
    scrap = Scraper("https://www.fox.co.il/en")
    main_categories_links = scrap.get_main_categories()
    assert_equal(main_categories_links, [u'https://www.fox.co.il/en/WOMEN',
                                         u'https://www.fox.co.il/en/men',
                                         u'https://www.fox.co.il/en/KIDS',
                                         u'https://www.fox.co.il/en/BABY',
                                         u'https://www.fox.co.il/en/international_2141146'])


def test_get_sub_categories():
    scrap = Scraper("https://www.fox.co.il/en")
    main_categories_links = scrap.get_main_categories()
    sub_categories_links = scrap.get_sub_categories(main_categories_links[0], 0)
    assert_equal(sub_categories_links, [u'https://www.fox.co.il/en/WOMEN/4143357/4143390',
                                        u'https://www.fox.co.il/en/WOMEN/4143357/4143358',
                                        u'https://www.fox.co.il/en/WOMEN/4143383',
                                        u'https://www.fox.co.il/en/WOMEN/4143456',
                                        u'https://www.fox.co.il/en/WOMEN/4143406/4143411',
                                        u'https://www.fox.co.il/en/WOMEN/4143406/4143409',
                                        u'https://www.fox.co.il/en/WOMEN/4143406/4143407',
                                        u'https://www.fox.co.il/en/WOMEN/4143449',
                                        u'https://www.fox.co.il/en/WOMEN/4143350',
                                        u'https://www.fox.co.il/en/WOMEN/4143343'])


def test_get_catalog_sub_category():
    scrap = Scraper("https://www.fox.co.il/en")
    main_categories_links = scrap.get_main_categories()
    scrap.get_sub_categories(main_categories_links[0], 0)
    sub_category_catalog = BeautifulSoup(str(catalog), 'html.parser')
    sub_catalog = scrap.get_sub_category_catalog(sub_category_catalog, 0, 0)
    items = [FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143405",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "119.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143404",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "81.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143403",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "129.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143402",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "119.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143397",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "119.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143393",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "79.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143391",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "119.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143474",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "129.9"),
             FoxItem("https://www.fox.co.il/en/WOMEN/4143357/4143390/4143477",
                     "WOMEN", "Shirts Woven/Denim", "SHIRT WOVEN", "119.9")]

    # @Caduri - plz advise - to compare the actual lists of the objects (FoxItem),
    # I could not do it directly, I needed to download a special package or do it the "hard way"
    # I created a new function in FoxItem class that returns all fields as complete string....
    # and... it look really f..up
    # what is the proper way to test it? I thought maybe compare the list using a simple "if" statement
    # (it works) and then use the assert_equal on the result. but it's feels like "cheating"
    for item_num in range(len(sub_catalog)):
        assert_equal(sub_catalog[item_num].print_assert(), items[item_num].print_assert())
        assert_equal(sub_catalog[item_num].print_assert(), items[item_num].print_assert())


