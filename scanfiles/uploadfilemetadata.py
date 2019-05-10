
import os
from django.conf import settings
from scanfiles.repofiles import File
from scanfiles.databaseupdate import DbModel
import time

def scanfiles():
    """
    This function will monitor the folder given in an interval of one hour
    and update the database if any new file has arrived or any file
    is changed in the last time given in the settings. 
    The case of files getting deleted is not taken into consideration. Even
    if the files are deleted from the folder, it will not be removed from
    the database or flagged in the database.
    """
    while True:
        print("Waiting seconds  :", settings.TIME_INTERVAL)
        with os.scandir(settings.FOLDER_PATH) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_file():
                    filedetails = File(entry.name, entry.path).filedetailsObj
                    if filedetails == None:
                        continue
                    else:
                        dbupdate = DbModel()
                        dbupdate.update_database(filedetails)    
        time.sleep(settings.TIME_INTERVAL)

if __name__ == '__main__':
    scanfiles()



