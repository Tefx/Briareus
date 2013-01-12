#!/usr/bin/env python

from setuptools import setup


requires = ["gevent>=0.13.0", "Corellia>=0.2.4", "Husky>=0.1.0"]
console_scripts=['Briareus-Worker=Briareus.Cloud.worker:run']

setup(name='Briareus',
      version='0.4.1',
      description='',
      author='Zhu Zhaomeng',
      author_email='zhaomeng.zhu@gmail.com',
      packages=['Briareus', 'Briareus.Cloud', 'Briareus.Parallel', 'Briareus.Face', 'Briareus.Lazy'],
      install_requires=requires,
      url="https://github.com/Tefx/Briareus",
      entry_points=dict(console_scripts=console_scripts),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Topic :: Utilities",
      ]
      )
