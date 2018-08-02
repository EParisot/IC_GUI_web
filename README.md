# IC_GUI_web
Images Classifier GUI web

## Architecture:
```
- Project
      - Apps
          - static
                css
                img
                scripts
          - templates
                html
          - python views, urls, models, ...
      - media
          - user
              - files
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

//create / update database
python manage.py makemigrations
python manage.py migrate

//run project
python manage.py runserver
```

and go to 127.0.0.1:8000...

