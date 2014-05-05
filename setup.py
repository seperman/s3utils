import os
from setuptools import setup #, find_packages

try:
    with open('README.md') as file:
        long_description = file.read()
except:
    long_description = "S3 Utils deals with Amazon S3 buckets"


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='s3utils',
      version='0.5.2',
      description='S3 Utils deals with Amazon S3 buckets',
      url='https://github.com/erasmose/s3utils',
      download_url='https://github.com/erasmose/s3utils/tarball/master',
      author='Erasmose',
      author_email='sep@zepworks.com',
      license='Apache License 2.0',
      packages=['s3utils'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "boto>=2.27.0",
      ],
      long_description=long_description,
      classifiers=[
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',        
        ],
      )