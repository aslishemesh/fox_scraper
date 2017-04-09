try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'FOX site scrapper',
    'author': 'Asli Shemesh',
    'url': 'N/A.',
    'download_url': 'N/A',
    'author_email': 'N/A',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['fox_scraper'],
    'scripts': [],
    'name': 'fox_scraper'
}

setup(**config)

