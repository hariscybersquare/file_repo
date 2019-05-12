import os
from datetime import datetime, timedelta


class File():
    """
    File stored in the directory. This class returns the
    data required for the database update.
    """

    def __init__(self, filename, filepath):

        filedetails = os.stat(filepath)
        if(datetime.fromtimestamp(filedetails.st_mtime)
                < (datetime.now() - timedelta(days=5))):
            self.filedetailsObj =\
                                (filename,
                                 filepath.rsplit('/' + filename, 1)[0],
                                 datetime.fromtimestamp(filedetails.st_ctime),
                                 datetime.fromtimestamp(filedetails.st_mtime),
                                 filedetails.st_size,
                                 True)
        elif(datetime.fromtimestamp(filedetails.st_mtime)
                < (datetime.now() - timedelta(hours=1))):
            self.filedetailsObj =\
                                (filename,
                                 filepath.rsplit('/' + filename, 1)[0],
                                 datetime.fromtimestamp(filedetails.st_ctime),
                                 datetime.fromtimestamp(filedetails.st_mtime),
                                 filedetails.st_size,
                                 False)
        else:
            self.filedetailsObj = None
