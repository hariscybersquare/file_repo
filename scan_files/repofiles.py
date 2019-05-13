import os
from datetime import datetime, timedelta
from scan_files.database_functions import DbModel


class File():
    """
    File stored in the directory. This class returns the
    data required for the database update.
    """

    def __init__(self, file_name, file_path):
        try:
            file_details = os.stat(file_path)

        except Exception as error:
            print("We could not run the stat command on the file. Please\
                   check to make sure that all permissions are set. ")
            print(error)
        try:
            db_obj = DbModel()
            last_modified_datatime = db_obj.get_last_updated_datetime()
            if not last_modified_datatime:
                try:
                    raise Exception("No data in the database.")
                except Exception as e:
                    print("There is no data in the database.")
                    print(e)
        except Exception as error:
            print("Some error while trying to retrieve the last updated\
                   time from the database.")
            print(error)
        '''
        The first if condition checks if the file is modified before
        5 days. If modified before 5 days, the status of the file
        will be changed to archived. This is achieved by setting the
        the archived flag = True. Currently the files are not moved
        to another folder. But it can also be done.
        '''
        try:
            if(datetime.fromtimestamp(file_details.st_mtime)
                    < (datetime.now() - timedelta(days=5))):
                self.file_details_Obj =\
                            (file_name,
                             file_path.rsplit('/' + file_name, 1)[0],
                             datetime.fromtimestamp(file_details.st_ctime),
                             datetime.fromtimestamp(file_details.st_mtime),
                             file_details.st_size,
                             True,
                             datetime.now(),
                             datetime.now())
                """
                The following condition will make sure that we are updating
                the files that are not yet updated from the last run of the
                process.Currently all the files will continue to be in the same
                folder. The following code will make sure that meta data of the
                files are uploaded even if one scanning job fails.
                """
            elif(datetime.fromtimestamp(file_details.st_mtime)
                    > last_modified_datatime):
                self.file_details_Obj =\
                            (file_name,
                             file_path.rsplit('/' + file_name, 1)[0],
                             datetime.fromtimestamp(file_details.st_ctime),
                             datetime.fromtimestamp(file_details.st_mtime),
                             file_details.st_size,
                             False,
                             datetime.now(),
                             datetime.now())
            else:
                self.file_details_Obj = None
        except Exception as e:
            print("something went wrong while createing file object.")
            print(e)
