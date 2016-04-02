#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
To run the test, run this in the root of repo:
python -m unittest discover

To run a specific test, run this from the root of repo:
python -m unittest tests.S3utilsTestCase.test_cp_folder_content
"""
import os
import unittest
import boto
from boto.s3.key import Key
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
        self.k = Key(self.bucket)

    @mock_s3
    def test_rm(self):
        self.setup_bucket()

        key = "somefile.txt"
        self.k.key = key
        self.k.set_contents_from_string("some content")

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        s3utils.rm(key)

        remote_files = self.bucket.list(prefix='', marker='')
        remote_files_names = [i.name for i in remote_files]

        self.assertEqual(remote_files_names, [])

    @mock_s3
    def test_rm_folder(self):
        self.setup_bucket()

        keys = ('/folder/file1.txt', '/folder/file2.txt', '/folder/folder2/file3.txt')
        for key in keys:
            self.k.key = key
            self.k.set_contents_from_string("some content")

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        s3utils.rm('/folder/')

        remote_files = self.bucket.list(prefix='', marker='')
        remote_files_names = [i.name for i in remote_files]

        self.assertEqual(remote_files_names, [])

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

    def copy_base(self, action):
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
        self.assertEqual(filecontent, remote_content.decode('utf-8'))

        return filepath_local

    def copy_folder_base(self, action, folder='/tmp/test_s3_folder', filepath_remote_prefix='test_s3_folder/'):
        self.setup_bucket()

        folder_local = '/tmp/test_s3_folder'
        filename_list = ['test_file_for_s3.txt', 'test_file_for_s3_b.txt']
        filecontent = 'this is the first line added using python'
        filepath_local_list = ['/tmp/test_s3_folder/%s' % filename for filename in filename_list]
        filepath_remote = '/somewhere_remote/'
        filepath_remote_on_s3_set_expected = {'somewhere_remote/%s%s' % (filepath_remote_prefix, filename) for filename in filename_list}

        if not os.path.exists(folder_local):
            os.makedirs(folder_local)

        for filepath_local in filepath_local_list:
            with open(filepath_local, 'w') as f:
                f.write(filecontent)

        s3utils = S3utils(AWS_STORAGE_BUCKET_NAME='testbucket')
        s3utils_result = getattr(s3utils, action)(folder, filepath_remote)

        remote_files = self.bucket.list(prefix='', marker='')
        remote_files_names = {i.name for i in remote_files}

        # If s3utils returns something, it means there was a problem
        if s3utils_result:
            self.assertEqual(remote_files_names, set([]))
        else:
            self.assertEqual(remote_files_names, filepath_remote_on_s3_set_expected)

            filepath_remote_on_s3 = next(iter(filepath_remote_on_s3_set_expected))
            remote_content = self.bucket.get_key(filepath_remote_on_s3).get_contents_as_string()
            self.assertEqual(filecontent, remote_content.decode('utf-8'))

        return (folder_local, s3utils_result)

    @mock_s3
    def test_cp(self):
        filepath_local = self.copy_base(action='cp')
        self.assertTrue(os.path.exists(filepath_local))

    @mock_s3
    def test_mv(self):
        filepath_local = self.copy_base(action='mv')
        self.assertFalse(os.path.exists(filepath_local))

    @mock_s3
    def test_cp_folder(self):
        folder_local, s3utils_result = self.copy_folder_base(action='cp')
        self.assertTrue(os.path.exists(folder_local))

    @mock_s3
    def test_mv_folder(self):
        folder_local, s3utils_result = self.copy_folder_base(action='mv')
        self.assertFalse(os.path.exists(folder_local))

    @mock_s3
    def test_cp_folder_content(self):
        folder_local, s3utils_result = self.copy_folder_base(action='cp', folder='/tmp/test_s3_folder/*', filepath_remote_prefix='')
        self.assertTrue(os.path.exists(folder_local))
        self.assertEqual(s3utils_result, None)

    @mock_s3
    def test_cp_folder_that_does_not_exist(self):
        folder_local, s3utils_result = self.copy_folder_base(action='cp', folder='/tmp/test_s3_folder_that_does_not_exist/', filepath_remote_prefix='')
        self.assertEqual(s3utils_result, {'file_does_not_exist': '/tmp/test_s3_folder_that_does_not_exist'})
