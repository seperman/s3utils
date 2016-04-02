.. S3utils documentation master file, created by
   sphinx-quickstart on Tue Apr 29 15:47:56 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to S3utils's documentation!
===================================

**S3utils is a simple interface for dealing with Amazon S3**

************
Installation
************

Install from PyPi::

    pip install s3utils

Python 2.7, 3.3, 3.4, 3.5 are supported.

*****
Setup
*****

Normal Setup
------------
    >>> from s3utils import S3utils
    >>> s3utils = S3utils(
    ... AWS_ACCESS_KEY_ID = 'your access key',
    ... AWS_SECRET_ACCESS_KEY = 'your secret key',
    ... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
    ... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
    ... )

or if you are using Django, simply:

Django Setup
------------
    >>> S3UTILS_DEBUG_LEVEL=1
    >>> AWS_ACCESS_KEY_ID = 'your access key'
    >>> AWS_SECRET_ACCESS_KEY = 'your secret key'
    >>> AWS_STORAGE_BUCKET_NAME = 'your bucket name'

And in your code:
    >>> from s3utils import S3utils
    >>> s3utils = S3utils()

If you want to overwrite your bucket name in your code from what it is in the Django settings:
    >>> from s3utils import S3utils
    >>> s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='some other bucket')


********
Commands
********

The commands are made to be similar to Linux file commands:

cp, mv, chmod, ls, ll, echo, mkdir, rm

There are some Cloudfront specific commands too:

invalidate

*************
S3utils 0.6.0
*************

.. toctree::
   :maxdepth: 2

.. automodule:: s3utils

.. autoclass:: S3utils
    :members:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Author
==================

Seperman (Sep Ehr)

* `Zepworks <http://zepworks.com>`_
* `Github <https://github.com/seperman>`_
* `Linkedin <http://www.linkedin.com/in/sepehr>`_
