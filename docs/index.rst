.. S3utils documentation master file, created by
   sphinx-quickstart on Tue Apr 29 15:47:56 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to S3utils's documentation!
===================================

** S3utils deals with files on Amazon S3 Bucket **

************
Installation
************

Install from PyPi::

    pip install s3utils


***************
Setup in Django
***************
    
in your settings file::

    S3UTILS_DEBUG_LEVEL=1
    AWS_ACCESS_KEY_ID = 'your access key'
    AWS_SECRET_ACCESS_KEY = 'your secret key'
    AWS_STORAGE_BUCKET_NAME = 'your bucket name'

in your code::

    from s3utils import S3utils
    s3utils = S3utils()

**************
Setup manually
**************

in your code::

    from s3utils import S3utils
    s3utils = S3utils(
    AWS_ACCESS_KEY_ID = 'your access key',
    AWS_SECRET_ACCESS_KEY = 'your secret key',
    AWS_STORAGE_BUCKET_NAME = 'your bucket name',
    S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
    )



*************
S3utils 0.5
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

Erasmose (Sep Dehpour)
`Github <https://github.com/erasmose>`_
`Linkedin <http://www.linkedin.com/in/sepehr>`_
