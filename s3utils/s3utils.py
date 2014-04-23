import os
import re
from boto.s3.connection import S3Connection
from boto.s3.key import Key

try:
    from django.conf import settings
except:
    class settings():
        AWS_ACCESS_KEY_ID=""
        AWS_SECRET_ACCESS_KEY=""
        AWS_STORAGE_BUCKET_NAME=""
        MEDIA_ROOT=""
        MEDIA_ROOT_BASE=""
        GO_S3_DEBUG_LEVEL=0

# LOGGING
try:
    from settings_logging import the_logging
except:
    import logging as the_logging


class S3utils(object):

    def __init__(
        self, AWS_ACCESS_KEY_ID=getattr(settings,"AWS_ACCESS_KEY_ID",""),
        AWS_SECRET_ACCESS_KEY=getattr(settings,"AWS_SECRET_ACCESS_KEY",""),
        AWS_STORAGE_BUCKET_NAME=getattr(settings,"AWS_STORAGE_BUCKET_NAME",""),
        MEDIA_ROOT=getattr(settings,"MEDIA_ROOT",""),
        MEDIA_ROOT_BASE=getattr(settings,"MEDIA_ROOT_BASE",""),
        GO_S3_DEBUG_LEVEL=getattr(settings,"GO_S3_DEBUG_LEVEL",0),
            ):

        self.AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
        self.AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
        self.AWS_STORAGE_BUCKET_NAME = AWS_STORAGE_BUCKET_NAME
        self.MEDIA_ROOT = MEDIA_ROOT
        self.MEDIA_ROOT_BASE = MEDIA_ROOT_BASE
        self.GO_S3_DEBUG_LEVEL = GO_S3_DEBUG_LEVEL

        self.logger = the_logging.getLogger(__name__)
        
        #setting the logging level based on GO_S3_DEBUG_LEVEL
        if (GO_S3_DEBUG_LEVEL==0):
            self.logger.setLevel(the_logging.ERROR)
        else:
            self.logger.setLevel(the_logging.WARNING)

    

    def connect(self):
        """establishes the connection"""

        self.conn = S3Connection(self.AWS_ACCESS_KEY_ID, self.AWS_SECRET_ACCESS_KEY, debug=self.GO_S3_DEBUG_LEVEL)

        self.bucket = self.conn.get_bucket(self.AWS_STORAGE_BUCKET_NAME)

        self.k = Key(self.bucket)



    def disconnect(self):
        """closes the connection"""
        
        self.bucket.connection.connection.close() 


    def cp_file(self, local_file, target_file, acl='public-read', del_after_upload=False):
        """ copies a file to s3 """

        print "----------------------"
        print "copying"
        print local_file
        print target_file
        # try:
        #     self.k.key = target_file   #setting the path (key) of file in the container
        #     self.k.set_contents_from_filename(local_file)  #grabs the contents from local_file address. Note that it loads the whole file into memory
        #     self.logger.info("uploaded to s3: %s" % target_file)  
        #     self.k.set_acl(acl)  #setting the file permissions
        #     self.k.close()  #not sure if it is needed. Somewhere I read it is recommended.

        #     #if it is supposed to delete the local file after uploading
        #     if del_after_upload:
        #         try:
        #             os.remove(local_file)
        #         except:
        #             self.logger.error("Unable to delete the file: ", exc_info=True)
        #             pass

        #     return True
        # except:
        #     self.logger.error(exc_info=True)
        #     return False


    def cp(self, local_path, target_path, acl='public-read', del_after_upload=False):
        """ copies a file or folder from local to s3"""


        if os.path.exists(local_path):
            
            #copying the contents of the folder and not folder itself
            if local_path.endswith("/*"):   
                local_path=local_path[:-2]
                target_path = re.sub(r"^/|/$", "", target_path)   #Amazon S3 doesn't let the name to begin with /
            #copying folder too
            else:
                local_path = re.sub(r"/$", "", local_path)
                target_path = os.path.join(
                                    re.sub(r"^/", "", target_path),
                                     os.path.basename(local_path)
                                     ) 

            #if it is a folder
            if os.path.isdir(local_path):

                re_base = re.compile(r"^"+local_path)  #matching for strings starting with local_path

                for local_root, directories, files in os.walk(local_path):

                    #if folder is not empty
                    if files:
                        #iterating over the files in the folder
                        for a_file in files:
                            self.cp_file(
                                        os.path.join(local_root, a_file),
                                        os.path.join(
                                            re_base.sub(local_root, target_path),
                                            a_file
                                            ),
                                        acl=acl,
                                        del_after_upload=del_after_upload,
                                        )
                    #if folder is empty
                    else:
                        #TODO: test copying an empty folder
                        pass

            else:
                self.cp_file(local_path, target_path, acl=acl, del_after_upload=del_after_upload)
        else:
            self.logger.error("trying to upload to s3 but file doesn't exist: %s" % local_path)
            return False


    def mv(self, local_file, target_file, acl='public-read'):
        """moves the file to the S3 (deletes the local copy)"""

        self.cp(local_file, target_file, acl='public-read', del_after_upload=True)


    def cp_cropduster_image(self, the_image_path, del_after_upload=False):
        """deals with cropduster images saving to S3"""


        #self.logger.info("CKeditor the_image_path: %s" % the_image_path)
        
        local_file = os.path.join(settings.MEDIA_ROOT, the_image_path)

        #only try to upload things if the origin cropduster file exists (so it is not already uploaded to the CDN)
        if os.path.exists(local_file): 

            the_image_crops_path = os.path.splitext(the_image_path)[0]
            the_image_crops_path_full_path = os.path.join(settings.MEDIA_ROOT, the_image_crops_path)
        

            self.cp(local_file = local_file,
                            target_file = os.path.join(settings.MEDIA_ROOT_BASE, the_image_path),
                            del_after_upload = del_after_upload,
                            )

            try:
                all_thumbs = os.listdir(the_image_crops_path_full_path)

                for i in all_thumbs:
                    self.cp(os.path.join(settings.MEDIA_ROOT, the_image_crops_path, i),
                                    os.path.join(settings.MEDIA_ROOT_BASE, the_image_crops_path, i),
                                    del_after_upload = del_after_upload,
                                    )

                #self.logger.info("del_after_upload: %s " % del_after_upload)
                if del_after_upload:
                    try:
                        #self.logger.info("trying to delete folder: %s " % the_image_crops_path_full_path)
                        os.rmdir(the_image_crops_path_full_path)
                    except:
                        self.logger.error("Unable to delete the folder: ", exc_info=True)
                        pass

            except OSError as e:
                if e.strerror == 'Not a directory':
                    pass

                if e.strerror == 'No such file or directory':
                    self.logger.error("file or folder doesn't exist for upload: %s" % all_thumbs)
                    pass



    def get_grants(self, target_file):
        """ 
        returns grant permission, grant owner, grant owner email and grant id  as a list.
        It needs you to set k.key to a key on amazon (file path) before running this.
        note that Amazon returns a list of grants for each file.

        a. private: Owner gets FULL_CONTROL. No one else has any access rights.
        b. public-read: Owners gets FULL_CONTROL and the anonymous principal is granted READ access.
        c. public-read-write: Owner gets FULL_CONTROL and the anonymous principal is granted READ and WRITE access.
        d. authenticated-read: Owner gets FULL_CONTROL and any principal authenticated as a registered Amazon S3 user is granted READ access

        """
        
        self.k.key = target_file

        the_grants = self.k.get_acl().acl.grants    
        
        grant_list = []

        for grant in the_grants:
            grant_list.append( (grant.permission, grant.display_name, grant.email_address, grant.id) )

        return grant_list


    def chmod(self, target_file, acl='public-read'):
        """
        sets permissions for a file

        a. private: Owner gets FULL_CONTROL. No one else has any access rights.
        b. public-read: Owners gets FULL_CONTROL and the anonymous principal is granted READ access.
        c. public-read-write: Owner gets FULL_CONTROL and the anonymous principal is granted READ and WRITE access.
        d. authenticated-read: Owner gets FULL_CONTROL and any principal authenticated as a registered Amazon S3 user is granted READ access
  
        """

        self.k.key = target_file   #setting the path (key) of file in the container
        self.k.set_acl(acl)  #setting the file permissions
        self.k.close()



    def ls(self, folder="", begin_from_file="", num=-1, get_grants=False):
        """
           gets the list of file names (keys) in a s3 folder
           num: number of results to return, by default it returns all results.
           This should be an integer.
           folder: which folder to list its files
           
           begin_from_file: which file to start from (key).
           This is usedful in case you are iterating over lists of files
        """

        #S3 object key can't start with /
        folder = re.sub(r"/$", "", folder)

        bucket_files = self.bucket.list(prefix=folder, marker=begin_from_file)

        list_of_files = []


        #in case listing grants
        if get_grants:
            for (i,v) in enumerate(bucket_files):
                file_dict={"name":v.name, "grants": self.get_grants(v.name),}
                list_of_files.append(file_dict)
                if i==num:
                    break

        else:
            for (i,v) in enumerate(bucket_files):
                list_of_files.append(v.name)
                if i==num:
                    break            

        return list_of_files



    def ll(self, folder="", begin_from_file="", num=-1):
        """
           gets the list of file names (keys) in a s3 folder and the file permissions
           num: number of results to return, by default it returns all results.
           This should be an integer.
           folder: which folder to list its files
           
           begin_from_file: which file to start from (key).
           This is usedful in case you are iterating over lists of files
        """
        return self.ls(folder="", begin_from_file="", num=-1, get_grants=True)


