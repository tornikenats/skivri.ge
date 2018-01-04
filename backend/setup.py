from setuptools import setup

setup(name='skivri.ge frontend',
      version='1.0',
      description='skivri.ge frontend application',
      author='Tornike Natsvlishvili',
      author_email='',
      license='MIT',
      url='http://skivri.ge',
      install_requires=[
          'Flask',
          'gunicorn',
          'peewee',
          'PyMySQL',
      ],
      )
