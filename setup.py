#!/usr/bin/python

from setuptools import setup, find_packages

import openaps
def readme():
    with open("README.md") as f:
        return f.read()

setup(name='openaps',
    version=openaps.__version__, # http://semver.org/
    description='DIY Open Source Artificial Pancreas System.',
    long_description=readme(),
    author="OpenAPS",
    author_email="bewest+openaps@gmail.com",
    # url="https://github.com/openaps/openaps",
    url="https://openaps.org/",
    packages=['openaps'],
    install_requires = [
      'pyserial', 'python-dateutil', 'argcomplete',
      'decocare', # 'dexcom_reader'
    ],
    dependency_links = [
      'http://github.com/compbrain/dexcom_reader/tarball/master',
      'http://github.com/bewest/decoding-carelink/tarball/master',
    ],
    scripts = [
      'bin/openaps',
      'bin/openaps-device',
      'bin/openaps-enact',
      'bin/openaps-suggest',
      'bin/openaps-get',
      'bin/git-openaps-init',
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Libraries'
    ],
    zip_safe=False,
)

#####
# EOF
