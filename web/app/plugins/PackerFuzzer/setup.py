# -*- coding: utf-8 -*-
"""
@Time ： 2024/4/30 1:01 PM
@Auth ： xinghe
@File ：setup.py
@IDE ：PyCharm
@Motto: live != end, love ++
"""
from setuptools import setup, find_packages

setup(
    name='PackerFuzzer',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'oneforall=PackerFuzzer.PackerFuzzer:main',
        ],
    },
    author='xxxx',
    author_email='xxxxx@example.com',
    description='arl 的 PackerFuzzer 插件',
    url='https://github.com/xxxxx/PackerFuzzer',
)