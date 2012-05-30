import sys
import os.path
from setuptools import setup, find_packages

readme = os.path.join(os.path.dirname(__file__), 'README.rst')
long_description = open(readme).read()

setup(
    name='i18n',
    version='0.1',
    author='Antonio Cuni',
    author_email='anto.cuni@gmail.com',
    packages=['i18n'],
    url='http://bitbucket.org/antocuni/i18n',
    license='BSD',
    description='Package to simplify the development of internationalized applications',
    long_description=long_description,
    keywords='i18n gettext pybabel translation',
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Internationalization",
        ],
    install_requires=['py'], # and also PyQT, but it doesn't work with
                             # setuptools :-(
)