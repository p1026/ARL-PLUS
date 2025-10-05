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
    name='OneForAll',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'oneforall=OneForAll.oneforall:main',
        ],
    },
    author='shmilylty',
    author_email='shmilylty@example.com',
    description='arl 的 oneforall 插件',
    url='https://github.com/shmilylty/OneForAll',
)