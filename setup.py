import os
from setuptools import setup  # , find_packages

try:
    with open('README.md') as file:
        long_description = file.read()
except:
    long_description = "S3 Utils deals with Amazon S3 buckets"

test_requirements = ['moto==0.4.23']

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(name='s3utils',
      version='0.6.0',
      description='S3 Utils deals with Amazon S3 buckets',
      url='https://github.com/seperman/s3utils',
      download_url='https://github.com/seperman/s3utils/tarball/master',
      author='Seperman',
      author_email='sep@zepworks.com',
      license='Apache License 2.0',
      packages=['s3utils'],
      include_package_data=True,
      zip_safe=False,
      tests_require=test_requirements,
      install_requires=[
          "boto>=2.39.0",
      ],
      long_description=long_description,
      classifiers=[
          'Environment :: Web Environment',
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Topic :: Software Development",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          "License :: OSI Approved :: Apache Software License"
      ],
      )
