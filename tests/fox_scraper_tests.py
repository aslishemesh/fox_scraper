from nose.tools import *
from fox_scraper.fox_scraper import Scraper


def test_scraper_initialization():
    scrap = Scraper("https://www.fox.co.il/en")
    assert_equal(scrap.site_address, "https://www.fox.co.il/en")
    assert_equal(scrap.main_categories, [])
    assert_equal(scrap.sub_categories, [])

def test_scraping_categories():
    main_categories_links = []
    sub_categories_links = []
    print "start"
    scrap = Scraper("https://www.fox.co.il/en")
    main_categories_links = scrap.scrap_fox_main_categories()
    print "Testing scraping main categories:\n"
    assert_equal(main_categories_links, [u'https://www.fox.co.il/en/WOMEN',
                                         u'https://www.fox.co.il/en/men',
                                         u'https://www.fox.co.il/en/KIDS',
                                         u'https://www.fox.co.il/en/BABY',
                                         u'https://www.fox.co.il/en/international_2141146'])
    print "================================================================="
    print "Testing scraping sub categories:\n"
    sub_categories_links = scrap.scrap_fox_sub_categories(main_categories_links[0], 0)
    print sub_categories_links
    assert_equal(main_categories_links, [u'https://www.fox.co.il/en/WOMEN/4143357/4143390',
                                         u'https://www.fox.co.il/en/WOMEN/4143357/4143358',
                                         u'https://www.fox.co.il/en/WOMEN/4143383',
                                         u'https://www.fox.co.il/en/WOMEN/4143456',
                                         u'https://www.fox.co.il/en/WOMEN/4143406/4143411',
                                         u'https://www.fox.co.il/en/WOMEN/4143406/4143409',
                                         u'https://www.fox.co.il/en/WOMEN/4143406/4143407',
                                         u'https://www.fox.co.il/en/WOMEN/4143449',
                                         u'https://www.fox.co.il/en/WOMEN/4143350',
                                         u'https://www.fox.co.il/en/WOMEN/4143343'])

    def test_scraping_sub_categories():

    print "================================================================="
"""
    catalog = []
    print "Scraping items for sub-category:\n"
    catalog = scrap.scrap_fox_catalog(sub_categories_links, 0)
    for item in catalog:
        item.print_item()
"""
def test_scraping_catalog():
    pass

def test_add():
    print "TEAR DOWN!"


def test_basic():
    print "I RAN!"

