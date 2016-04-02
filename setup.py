import os
from setuptools import setup  # , find_packages

# if you are not using vagrant, just delete os.link directly,
# The hard link only saves a little disk space, so you should not care
if os.environ.get('USER', '') == 'vagrant':
    del os.link

try:
    with open('README.txt') as file:
        long_description = file.read()
except:
    long_description = "S3utils is a simple interface to Amazon S3 Buckets."

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
          "Programming Language :: Python :: 3.3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          "License :: OSI Approved :: Apache Software License"
      ],
      )
