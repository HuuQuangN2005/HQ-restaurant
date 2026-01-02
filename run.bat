@echo off
cd /d %~dp0

call venv\Scripts\activate

cd restaurant

call python .\manage.py runserver
pause    