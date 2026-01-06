@echo off
cd /d %~dp0

call python -m venv venv
call venv\Scripts\activate

cd restaurant
call pip install -r .\requirements.txt


call python .\manage.py makemigrations
call python .\manage.py migrate

call python .\data.py
call python .\manage.py createsuperuser

pause   