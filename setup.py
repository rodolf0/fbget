#!/usr/bin/env python2

from setuptools import setup, find_packages

setup(
  name="fbget",
  version="0.1",
  packages=find_packages(),

  install_requires=["oauth2client", "httplib2"],

  include_package_data = True,

  entry_points={
    'console_scripts': [
      'fbget = fbget.__main__:main',
    ]
  },

  author="Rodolfo Granata",
  author_email="warlock.cc@gmail.com",
  description="a tool to collect my fb stuff",
)
