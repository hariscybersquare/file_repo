# file_repo
This is done as a part of a coding test. 

## Basic configuration:


Steps: 

1. Start your virtual environment
2. Create a folder name "yourfilename" (In the terminal, type ```mkdir "yourfilename"``` )
3. ```cd "yourfilenamemckdir"``` 
4. At the terminal, type 
   
   ```
   git clone https://github.com/harisnp/file_repo.git
   ```
5. Type 
```pip install -r requirements.txt```
6. Configure the filepath by going to settings.py in the line number 19 by setting the variable FOLDER_PATH.
7. Configure the interval of running the file scanner in the line number 22 by setting the variable TIME_INTERVAL.
8. Configure how many times you want to repeat the scanning in the line number 25 by setting the variable SCANNING_NUMBER. This is done just to make the testing easier as the process will stop after the specified scanning.  
9. You can enable or disable the authenticaion part by setting the AUTHENTICATION_ON to True or False in the line number 28. Please note that if the AUTHENTICATION_ON is set to False, one of the test case will fail.
10. Configure the database by providing database details in the line number 93

	```
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql',
	        'HOST': "127.0.0.1",
	        'NAME': "******",
	        'USER': "******",
	        'PASSWORD': "*****",
	    }
	}
	```


	```
	python manage.py makemigrations
	python mange.py migrate
	```

## How can you test?

1. Create a folder or point the FOLDER_PATH to the existing path. Please make sure that there are files which are older than 5 days.
2. Set all the variables explained in the section how to run the app. 
3. Run in the terminal

   ```
   python manage.py runserver
   ```
4. Open a browser and type ```http://127.0.0.1:8000/api/filesapp/True/``` and ```http://127.0.0.1:8000/api/filesapp/False/``` - Please make sure to set the authentication to OFF otherwise, you will have to create a token which is not done as it is beyond the scope of the project. 
5.  If you want to test with authentication, you can type ```python manage.py test``` as it is implemented in TDD.

##  How it works?

As soon as the Django starts running, a thread will continue to run to scan the files. The following code 
```

    if(len(sys.argv)>0):
        if(sys.argv[1] == 'runserver'):
            thread1 = threading.Thread(target=scanfiles)
            if(thread1.is_alive() is False):
                thread1.start()

``` 
in the manage.py takes care of this part and the file metadata information is stored to the table file_repo. The API http://127.0.0.1:8000/api/filesapp/True/ returns the archived files and http://127.0.0.1:8000/api/filesapp/False/ returns the unarchived files. 

The business logic is that all the files which is more than 5 days will be in the status of archived.

## Thought process

For the scan and upload, ORM is not used to improve the performance. I have tested it more than 500000 files and it was loaded into the datase in 3 minutes.

## Test preparation 

The following code can be used to generate test file. You can specify the file location and the number of files that you want to create for the test.
```

import os
import time
import datetime
import random

FILELOCATION = "textfiles"
NUMBEROFFILES = 10000


class RepoFile():
    """
    For creating the file object.
    """
    def __init__(self, fileLocation, number):

        with open(fileLocation, "w") as f:
            f.write("This file is created for the coding test. ")
            f.write("\nThis is my second line of code with {} as \
                    the starting name.".format(number))
            f.write("\nThis line is the last line in the code.")


def getTimeStamp(nof, i):
    """
    Half of the files will be before 5 days and half of the files will
    be within 5 days.
    """
    now = datetime.datetime.now()
    hour = random.randint(0, 23)
    if(i < nof//2):
        day = now.day - random.randint(1, 5) if now.day > 5 else now.day
        year = now.year
    else:
        year = random.randint(2000, now.year - 1)
        day = now.day
    date = datetime.datetime(year=year, month=now.month, day=day,
                             hour=hour, minute=now.minute, second=now.second)
    return time.mktime(date.timetuple())


for i in range(1, NUMBEROFFILES+1):
    fileLocation = FILELOCATION + "/{}hello_world.txt".format(i)
    repofile = RepoFile(fileLocation, i)
    os.utime(fileLocation, (getTimeStamp(NUMBEROFFILES, i), 
                            getTimeStamp(NUMBEROFFILES, i)))

```

