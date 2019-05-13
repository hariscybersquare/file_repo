
import os
from django.conf import settings
from scan_files.repofiles import File
from scan_files.database_functions import DbModel
import time


def scan_files():
    """
    This function will monitor the folder given in an interval of one hour
    and update the database if any new file has arrived or any file
    is changed in the last time given in the settings.
    The case of files getting deleted is not taken into consideration. Even
    if the files are deleted from the folder, it will not be removed from
    the database or flagged in the database.
    """
    number_of_times = 1
    while True:
        number_of_times += 1
        file_details = []
        try:
            with os.scandir(settings.FOLDER_PATH) as it:
                for entry in it:
                    if not entry.name.startswith('.') and entry.is_file():
                        file_detail_obj = File(entry.name,
                                               entry.path).file_details_Obj
                        if file_detail_obj:
                            file_details.append(file_detail_obj)
            if len(file_details) > 0:
                db_update = DbModel()
                db_update.update_database(tuple(file_details))
            time.sleep(settings.TIME_INTERVAL)
            if(number_of_times > settings.SCANNING_NUMBER):
                break
        except FileNotFoundError as e:
            print("Please provide a valid file path.")
            print(e)
            break
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    scan_files()
