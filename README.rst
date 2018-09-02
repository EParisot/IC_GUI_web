IC_GUI_web
==========

.. image:: https://img.shields.io/pypi/v/pip.svg
   :target: https://pypi.org/project/pip/
.. image:: https://img.shields.io/badge/Django-2.0-green.svg
   :target: https://pypi.org/project/Django/

(this project is a Django/web version of https://github.com/EParisot/ImagesClassifier_GUI (Python/Tkinter standalone app))

.. image:: /screenshot_IC_GUI.bmp

Machine Learning Images Classification in Graphical User Interface
* Take pictures
* Labelize them
* Define a Model Design
* Train your model 
* Test your model

Without any line of code, on any device !
-----------------------------------------

.. image:: /screenshot_model.bmp

.. image:: /screenshot_training.bmp

Installation:
-----------------------------------------

Windows users or 42 students :
------------------------------
Install Anaconda 3 :

https://www.continuum.io/downloads
or
https://github.com/42-AI/ai-for-42-students/blob/master/HOW_TOs.md

Install all dependencies listed in requirements.txt :
``
sudo pip install -r requirements.txt
``


Linux users :
-------------
``sudo apt-get install python3-pip`` and ``sudo pip3 install -r requirements.txt``


-----------------------------------------

Then :
``
cd ImagesClassifier
``

- create / update database
``
python manage.py migrate
``

- create superuser
``
python manage.py createsuperuser
``

- run project
``
python manage.py runserver
``

and go to 127.0.0.1:8000 to test it localy

To use another IP address and serve IC_GUI on your network, simply add it to ALLOWED_HOSTS in settings.py and run with:
``python manage.py runserver IP``

Enjoy it !
----------