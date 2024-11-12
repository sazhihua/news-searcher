@echo off

title News Searcher Server

echo Listening for the Port: 5200
echo Please visit http://127.0.0.1:5200/

python manage.py runserver --noreload 0.0.0.0:5200

