from setuptools import setup, find_packages
import os

version = '0.9'
description = open("README.txt").read() + "\n"
description += open(os.path.join("docs", "HISTORY.txt")).read()

setup(
    name='edeposit.amqp',
    version=version,
    description="E-Deposit AMQP Common Package",
    long_description=description,
    url='https://github.com/jstavel/edeposit.amqp/',

    author='Edeposit team',
    author_email='',

    classifiers=[
        "Programming Language :: Python",
    ],

    keywords='',
    license='GPL',

    packages=find_packages(exclude=['ez_setup']),

    namespace_packages=['edeposit'],
    include_package_data=True,
    zip_safe=False,
    test_suite='edeposit.amqp.tests',
    install_requires=[
        'setuptools',
        "python-daemon>=1.5.5"
    ],
    # entry_points="""
    # # -*- Entry points: -*-
    # """,
)
