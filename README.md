# S3 Utils v0.6.0

![Python Versions](https://img.shields.io/pypi/pyversions/s3utils.svg?style=flat)
![Doc](https://readthedocs.org/projects/s3utils/badge/?version=latest)
![License](https://img.shields.io/pypi/l/s3utils.svg?version=latest)
[![Build Status](https://travis-ci.org/seperman/s3utils.svg?branch=master)](https://travis-ci.org/seperman/s3utils)

User friendly interface to deal with Amazon S3 bucket and Cloud Front in Python.
I wrote this since s3cmd is for commandline usage and the other libraries out there seemed to be not maintained anymore.

The s3utils methods are made to be just like Linux commands so it is easy to remember and use.

Behind the scene it is a light Python wrapper around Amazon Boto library.

## Supported Python versions

Python 2.7, 3.3, 3.4 and 3.5 are supported.


## Documentation
* [Documentations](http://s3utils.readthedocs.org/en/latest/)


## Installation

Install from PyPi:

    pip install s3utils

## Setup

## Example setup in Django


in your settings file::

```python
S3UTILS_DEBUG_LEVEL=1
AWS_ACCESS_KEY_ID = 'your access key'
AWS_SECRET_ACCESS_KEY = 'your secret key'
AWS_STORAGE_BUCKET_NAME = 'your bucket name'
```

in your code::

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils()
>>> s3utils.cp("path/to/folder","/test/")
copying /path/to/myfolder/test2.txt to test/myfolder/test2.txt
copying /path/to/myfolder/test.txt to test/myfolder/test.txt
copying /path/to/myfolder/hoho/photo.JPG to test/myfolder/hoho/photo.JPG
copying /path/to/myfolder/hoho/haha/ff to test/myfolder/hoho/haha/ff
```

## Example manual setup

```python
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
```

## Mkdir

Create a folder on S3.

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> s3utils.mkdir("path/to/my_folder")
Making directory: path/to/my_folder
```

## Cp

Copy a file or folder from local to s3

### Parameters

local_path : string
Path to file or folder. Or if you want to copy only the contents of folder, add /* at the end of folder name

target_path : string
Target path on S3 bucket.

acl : string, optional

File permissions on S3. Default is public-read

acl options:

- private: Owner gets FULL_CONTROL. No one else has any access rights.
- public-read: Owners gets FULL_CONTROL and the anonymous principal is granted READ access.
- public-read-write: Owner gets FULL_CONTROL and the anonymous principal is granted READ and WRITE access.
- authenticated-read: Owner gets FULL_CONTROL and any principal authenticated as a registered Amazon S3 user is granted READ access

del_after_upload : boolean, optional

delete the local file after uploading. This is effectively like moving the file.
You can use s3utils.mv instead of s3utils.cp to move files from local to S3.
It basically sets this flag to True.
default = False

overwrite : boolean, optional

overwrites files on S3 if set to True. Default is True

invalidate : boolean, optional

invalidates the CDN (a.k.a Distribution) cache if the file already exists on S3
default = False
Note that invalidation might take up to 15 minutes to take place. It is easier and faster to use cache buster
to grab lastest version of your file on CDN than invalidation.

Examples

```python
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

>>> # When overwrite is set to False:
>>> s3utils.cp("path/to/folder","/test/", overwrite=False)
test/myfolder/test2.txt already exist. Not overwriting.
test/myfolder/test.txt already exist. Not overwriting.
test/myfolder/hoho/photo.JPG already exist. Not overwriting.
test/myfolder/hoho/haha/ff already exist. Not overwriting.

>>> # To overwrite the files on S3 and invalidate the CDN (cloudfront) cache so the new file goes on CDN:
>>> s3utils.cp("path/to/folder","/test/", overwrite=True, invalidate=True)
copying /path/to/myfolder/test2.txt to test/myfolder/test2.txt
copying /path/to/myfolder/test.txt to test/myfolder/test.txt
copying /path/to/myfolder/hoho/photo.JPG to test/myfolder/hoho/photo.JPG
copying /path/to/myfolder/hoho/haha/ff to test/myfolder/hoho/haha/ff
```

## Mv

Move the file to the S3 and deletes the local copy

It is basically s3utils.cp that has del_after_upload=True

Examples

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> s3utils.mv("path/to/folder","/test/")
moving /path/to/myfolder/test2.txt to test/myfolder/test2.txt
moving /path/to/myfolder/test.txt to test/myfolder/test.txt
moving /path/to/myfolder/hoho/photo.JPG to test/myfolder/hoho/photo.JPG
moving /path/to/myfolder/hoho/haha/ff to test/myfolder/hoho/haha/ff
```

## Chmod

sets permissions for a file on S3

Parameters

target_file : string
Path to file on S3

acl : string, optional
File permissions on S3. Default is public-read

options:

- private: Owner gets FULL_CONTROL. No one else has any access rights.
- public-read: Owners gets FULL_CONTROL and the anonymous principal is granted READ access.
- public-read-write: Owner gets FULL_CONTROL and the anonymous principal is granted READ and WRITE access.
- authenticated-read: Owner gets FULL_CONTROL and any principal authenticated as a registered Amazon S3 user is granted READ access


Examples

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> s3utils.chmod("path/to/file","private")
```

## Ls

gets the list of file names (keys) in a s3 folder

Parameters

folder : string
Path to file on S3

num: integer, optional
number of results to return, by default it returns all results.

begin_from_file: string, optional
which file to start from on S3.
This is usedful in case you are iterating over lists of files and you need to page the result by
starting listing from a certain file and fetching certain num (number) of files.


Examples

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> print s3utils.ls("test/")
[u'test/myfolder/', u'test/myfolder/em/', u'test/myfolder/hoho/', u'test/myfolder/hoho/.DS_Store', u'test/myfolder/hoho/haha/', u'test/myfolder/hoho/haha/ff', u'test/myfolder/hoho/haha/photo.JPG']
```

## LL

Get the list of files and permissions from S3

Parameters

folder : string
Path to file on S3

num: integer, optional
number of results to return, by default it returns all results.

begin_from_file : string, optional
which file to start from on S3.
This is usedful in case you are iterating over lists of files and you need to page the result by
starting listing from a certain file and fetching certain num (number) of files.

all_grant_data : Boolean, optional
More detailed file permission data will be returned.

Examples

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> import json
>>> # We use json.dumps to print the results more readable:
>>> my_folder_stuff = s3utils.ll("/test/")
>>> print json.dumps(my_folder_stuff, indent=2)
{
  "test/myfolder/": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    }
  ],
  "test/myfolder/em/": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    }
  ],
  "test/myfolder/hoho/": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    }
  ],
  "test/myfolder/hoho/.DS_Store": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    },
    {
      "name": null,
      "permission": "READ"
    }
  ],
  "test/myfolder/hoho/haha/": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    }
  ],
  "test/myfolder/hoho/haha/ff": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    },
    {
      "name": null,
      "permission": "READ"
    }
  ],
  "test/myfolder/hoho/photo.JPG": [
    {
      "name": "owner's name",
      "permission": "FULL_CONTROL"
    },
    {
      "name": null,
      "permission": "READ"
    }
  ],
}
```

## Invalidate CDN

Invalidate the CDN (distribution) cache for a certain file of files. This might take up to 15 minutes to be effective.

You can check for the invalidation status using check_invalidation_request.

Examples

```python
>>> from s3utils import S3utils
>>> s3utils = S3utils(
... AWS_ACCESS_KEY_ID = 'your access key',
... AWS_SECRET_ACCESS_KEY = 'your secret key',
... AWS_STORAGE_BUCKET_NAME = 'your bucket name',
... S3UTILS_DEBUG_LEVEL = 1,  #change it to 0 for less verbose
... )
>>> aa = s3utils.invalidate("test/myfolder/hoho/photo.JPG")
>>> print aa
('your distro id', u'your request id')
>>> invalidation_request_id = aa[1]
>>> bb = s3utils.check_invalidation_request(*aa)
>>> for inval in bb:
...     print 'Object: %s, ID: %s, Status: %s' % (inval, inval.id, inval.status)
```

##Author

Seperman (Sep Ehr)

* [Zepworks.com](https://zepworks.com)
* [Github](https://github.com/seperman)
* [Linkedin](http://www.linkedin.com/in/sepehr)
