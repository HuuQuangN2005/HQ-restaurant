@echo off
cd /d %~dp0
call C:\Users\Admin\AppData\Local\Programs\Python\Python312\python.exe -m venv venv
call venv\Scripts\activate
call pip install -r .\requirements.txt

call python restaurant.manager makemigrations
pause   