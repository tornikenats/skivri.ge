from setuptools import setup

setup(name='skivri.ge scraper',
      version='1.0',
      description='skivri.ge scraper application',
      author='Tornike Natsvlishvili',
      author_email='',
      license='MIT',
      url='http://skivri.ge',
      install_requires=[
          'beautifulsoup4',
          'peewee',
          'pytz',
          'python-dateutil',
          'feedparser',
          'PyMySQL',
          'lxml',
          'prometheus-client'
      ],
      )
