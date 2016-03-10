from setuptools import setup

setup(
    name    = 'Ypip',
    version = '0.0.1',
    license = 'MIT',

    description = 'Recursive pip for VCS-based packages',
    long_description = open().read('README.rst'),
    
    scripts = ['ypip/ypip']
)
