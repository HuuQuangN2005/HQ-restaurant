@echo off
cd /d %~dp0

call python -m venv venv
call venv\Scripts\activate

cd restaurant
call pip install -r .\requirements.txt

pause   