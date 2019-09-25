#!/usr/bin/env python
# -*-coding:utf-8-*-

import codecs
import shutil
import sys

from setuptools import setup, find_packages

is_windows = 'win32' == sys.platform.lower()


def long_description():
    try:
        with codecs.open('README.md', encoding='utf-8') as f:
            return f.read()
    except Exception as e:  # 免得因为这个出现安装错误
        return "a simple image process tools."


REQUIREMENTS = ['pillow', 'click']

data_files_list = []
if not shutil.which('pdftocairo'):
    print('warning, can not found the pdftocairo command.')
    if is_windows:
        print('i will copy the pdftocairo.exe to the python Scripts folder.')
        print('please make sure your windows system has add the search path.')
        data_files_list.append(('Scripts', ['Scripts/pdftocairo.exe']))

setup(
    name='ximage',
    version='0.2.0',
    description='a simple image process tools.',
    long_description=long_description(),
    url='https://github.com/a358003542/ximage',
    author='cdwanze',
    author_email='a358003542@gmail.com',
    platforms='Linux, windows',
    keywords=['ximage', 'python'],
    license='MIT',
    classifiers=['License :: OSI Approved :: MIT License',
                 'Operating System :: Microsoft',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 3'],
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    zip_safe=False,
    include_package_data=True,
    data_files=data_files_list,
    setup_requires=REQUIREMENTS,
    install_requires=REQUIREMENTS,
    entry_points={
        'console_scripts': [
            'ximage=ximage.__main__:main',
        ]
    }
)
