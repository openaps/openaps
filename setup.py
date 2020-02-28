#!/usr/bin/env python3
from setuptools import find_packages, setup

import openaps


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="openaps",
    version=openaps.__version__,  # http://semver.org/
    description="DIY Open Source Artificial Pancreas System.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Ben West",
    author_email="bewest+openaps@gmail.com",
    # url="https://github.com/openaps/openaps",
    url="https://openaps.org/",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "pyserial",
        "python-dateutil",
        "argcomplete",
        "gitpython",
        "decocare >= 0.1.0",
        "dexcom_reader >= 0.2.0",
    ],
    extras_require={
        "testing": ["pytest"],
    },
    dependency_links=[
        "http://github.com/openaps/dexcom_reader/tarball/master#egg=dexcom_reader-master",
        # 'https://github.com/bewest/dexcom_reader/tarball/master#egg=dexcom_reader-0.0.7-dev-1',
        # 'https://github.com/bewest/decoding-carelink/tarball/master#egg=decocare-master',
        # 'https://github.com/bewest/decoding-carelink/tarball/dev#egg=decocare-0.0.20-dev-1',
    ],
    scripts=[
        "bin/openaps",
        "bin/openaps-device",
        "bin/openaps-use",
        "bin/openaps-report",
        "bin/openaps-vendor",
        "bin/openaps-alias",
        "bin/openaps-import",
        # 'bin/openaps-export',
        "bin/git-openaps-init",
        "bin/openaps-install-udev-rules",
    ],
    entry_points={
        "openaps.importable": [
            "vendors = openaps.vendors.plugins",
            "devices = openaps.devices",
            "reports = openaps.reports",
            "aliases = openaps.alias",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries",
    ],
    zip_safe=False,
)

#####
# EOF
