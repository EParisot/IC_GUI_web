# IC_GUI_web
Images Classifier GUI web

## Architecture:
```
- Project
      - Apps
          - templates
                html (base.html in main app, contents in other apps)
          - python views, urls, models, ...
      - media
          - user
              - files
      - static
            css
            img
            scripts
```

## Installation:

Windows users or 42 students :
Install Anaconda :

https://www.continuum.io/downloads
or
https://github.com/42-AI/ai-for-42-students/blob/master/HOW_TOs.md

Install all dependencies listed in requirements.txt (pip install <package_name>)

Then :
```
cd ImagesClassifier
```

//create / update database
```
python manage.py makemigrations
python manage.py migrate
```

//create superuser
```
python manage.py createsuperuser
```

//run project
```
python manage.py runserver
```

and go to 127.0.0.1:8000...

(to use another IP address, simply add it to ALLOWED_HOSTS in settings.py and run ```python manage.py runserver myOtherIP```)