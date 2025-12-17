#!/usr/bin/env python3
"""
Setup script for ZIP Archive Manager
"""

from setuptools import setup, find_packages
import os

# Read README for long description
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zip-archive-manager',
    version='3.2.0',
    description='Advanced ZIP Archive Manager with GUI and CLI',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='ZIP Archive Manager Team',
    url='https://github.com/Nady-Emad/ZIP-Archive-Manager',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
    ],
    entry_points={
        'console_scripts': [
            'zip-manager=cli.main:main',
            'zip-manager-gui=zip_manager_gui:main',
        ],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Topic :: System :: Archiving :: Compression',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
        'Environment :: X11 Applications :: Qt',
    ],
    python_requires='>=3.7',
    keywords='zip archive compression gui cli pyqt5 extraction password',
    project_urls={
        'Bug Reports': 'https://github.com/Nady-Emad/ZIP-Archive-Manager/issues',
        'Source': 'https://github.com/Nady-Emad/ZIP-Archive-Manager',
    },
)
