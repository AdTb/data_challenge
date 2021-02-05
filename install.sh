# Installation script for linux

#!/bin/bash


echo'Installation of the dependencies'
pip3 install -r requirements.txt
python manage.py migrate
echo 'Creating the administration account'
python manage.py createsuperuser
echo 'You can now launch a development server using the command `python manage.py runserver`' 
