from setuptools import setup

setup(
    name    = 'Ypip',
    version = '0.0.1',
    license = 'MIT',

    description = 'Recursive pip for VCS-based packages',
    long_description = open('README.rst').read(),

    scripts = ['ypip/ypip']
)
