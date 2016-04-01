#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To run the test, run this in the root of repo:
python -m unittest discover

To run a specific test, run this from the root of repo:
python -m unittest tests.S3utilsTestCase.test_list_of_sets_difference_ignore_order
"""
import os.path
import unittest
import boto
from moto import mock_s3
from s3utils import S3utils
from sys import version

py3 = version[0] == '3'


class S3utilsTestCase(unittest.TestCase):

    """S3utils Tests."""

    def setup_bucket(self):
        self.conn = boto.connect_s3()
        self.conn.create_bucket('testbucket')
        self.bucket = self.conn.get_bucket('testbucket')

    @mock_s3
    def test_mkdir(self):
        self.setup_bucket()

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        s3utils.mkdir("folder")

        remote_files = self.bucket.list(prefix='', marker='')
        remote_folder = [i.name for i in remote_files][0]
        self.assertEqual(remote_folder, "folder/")

    @mock_s3
    def test_mkdir2(self):
        self.setup_bucket()

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        s3utils.mkdir("/folder/")

        remote_files = self.bucket.list(prefix='', marker='')
        remote_folder = [i.name for i in remote_files][0]
        self.assertEqual(remote_folder, "folder/")

    def copy_base_tst(self, action):
        self.setup_bucket()

        filename = 'test_file_for_s3.txt'
        filecontent = 'this is the first line added using python'
        filepath_local = '/tmp/%s' % filename
        filepath_remote = '/somewhere_remote/'
        filepath_remote_on_s3 = 'somewhere_remote/%s' % filename

        with open(filepath_local, 'w') as f:
            f.write(filecontent)

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        getattr(s3utils, action)(filepath_local, filepath_remote)

        remote_files = self.bucket.list(prefix='', marker='')
        remote_folder = [i.name for i in remote_files][0]
        self.assertEqual(remote_folder, filepath_remote_on_s3)

        remote_content = self.bucket.get_key(filepath_remote_on_s3).get_contents_as_string()
        self.assertEqual(filecontent, remote_content)

        return filepath_local

    @mock_s3
    def test_cp(self):
        filepath_local = self.copy_base_tst(action='cp')
        self.assertTrue(os.path.exists(filepath_local))

    @mock_s3
    def test_mv(self):
        filepath_local = self.copy_base_tst(action='mv')
        self.assertFalse(os.path.exists(filepath_local))

