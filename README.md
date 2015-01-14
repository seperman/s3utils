##S3 Utils v0.5.3
=====

A light Python wrapper around Amazon Boto library.

##Documentation
* [Documentations](http://s3utils.readthedocs.org/en/latest/)


##Installation

Install from PyPi:

    pip install s3utils

##Example usage in Django


in your settings file::

    S3UTILS_DEBUG_LEVEL=1
    AWS_ACCESS_KEY_ID = 'your access key'
    AWS_SECRET_ACCESS_KEY = 'your secret key'
    AWS_STORAGE_BUCKET_NAME = 'your bucket name'

in your code::

    >>> from s3utils import S3utils
    >>> s3utils = S3utils()
    >>> s3utils.cp("path/to/folder","/test/")
    copying /path/to/myfolder/test2.txt to test/myfolder/test2.txt
    copying /path/to/myfolder/test.txt to test/myfolder/test.txt
    copying /path/to/myfolder/hoho/photo.JPG to test/myfolder/hoho/photo.JPG
    copying /path/to/myfolder/hoho/haha/ff to test/myfolder/hoho/haha/ff


##Example manual setup

    >>> from s3utils import S3utils
    >>> s3utils = S3utils(
    ... AWS_ACCESS_KEY_ID = 'your access key',
    ... AWS_SECRET_ACCESS_KEY = 'your secret key',
    ... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
    ... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
    ... )
    >>> s3utils.cp("path/to/folder","/test/")
    copying /path/to/myfolder/test2.txt to test/myfolder/test2.txt
    copying /path/to/myfolder/test.txt to test/myfolder/test.txt
    copying /path/to/myfolder/hoho/photo.JPG to test/myfolder/hoho/photo.JPG
    copying /path/to/myfolder/hoho/haha/ff to test/myfolder/hoho/haha/ff


##Example invalidate CDN cache of files that get overwritten

    >>> s3utils.cp("path/to/folder","/test/", invalidate=True)


##Author

Erasmose (Sep Dehpour)
* [Github](https://github.com/erasmose)
* [Linkedin](http://www.linkedin.com/in/sepehr)
