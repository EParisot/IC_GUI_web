# IC_GUI_web

(this project is a Django/web version of https://github.com/EParisot/ImagesClassifier_GUI (Python/Tkinter standalone app))

![Alt text](/screenshot_IC_GUI.bmp?raw=true "IC_GUI")

Machine Learning Images Classification in Graphical User Interface
* Take pictures
* Labelize them
* Define a Model Design
* Train your model 
* Test your model

### Without any line of code, on any device !

![Alt text](/screenshot_model.bmp?raw=true "Model")

![Alt text](/screenshot_training.bmp?raw=true "Training")

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

and go to 127.0.0.1:8000 to test it localy

To use another IP address and serve IC_GUI on your network, simply add it to ALLOWED_HOSTS in settings.py and run ```python manage.py runserver IP```

Enjoy it !
