#!/usr/bin/env python
# -*-coding:utf-8-*-

import codecs

from setuptools import setup, find_packages

def long_description():
    try:
        with codecs.open('README.md', encoding='utf-8') as f:
            return f.read()
    except Exception as e: # 免得因为这个出现安装错误
        return "a simple image process tools."


REQUIREMENTS = []


setup(
    name='ximage',
    version= '0.1.1',
    description='a simple image process tools.',
    long_description=long_description(),
    url = 'https://github.com/a358003542/ximage',
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
    setup_requires=REQUIREMENTS ,
    install_requires=REQUIREMENTS ,
    entry_points={
        'console_scripts': [
            'ximage=ximage.__main__:main',
        ]
    }
)
