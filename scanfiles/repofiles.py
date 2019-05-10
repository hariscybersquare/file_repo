import os 
from datetime import datetime, timedelta

class File():
    """
    File stored in the directory. This class returns the
    data required for the database update.
    """

    def __init__(self, filename, filepath):

        filedetails = os.stat(filepath)
        if(datetime.fromtimestamp(filedetails.st_mtime)<(datetime.now() - timedelta(hours = 1))):
            self.filedetailsObj = {
            'name': filename,
            'filepath' : filepath.rsplit('/'+ filename, 1)[0],
            'creationdatetime': datetime.fromtimestamp(filedetails.st_ctime),
            'modificationdatetime':  datetime.fromtimestamp(filedetails.st_mtime),
            'size': filedetails.st_size, 
            'archived': False
            }
        elif(datetime.fromtimestamp(filedetails.st_mtime)<(datetime.now() - timedelta(days = 5))):
            self.filedetailsObj = {
            'name': filename,
            'filepath' : filepath.rsplit('/'+ filename, 1)[0],
            'creationdatetime': datetime.fromtimestamp(filedetails.st_ctime),
            'modificationdatetime':  datetime.fromtimestamp(filedetails.st_mtime),
            'size': filedetails.st_size, 
            'archived': True
            }
        else:
            self.filedetailsObj = None 
