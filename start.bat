@echo off

cd /d C:\Users\San\Desktop\yareklama

python rek.py

if errorlevel 1 (
  echo Ошибка в скрипте rek.py
  pause
  exit /b 1
  goto :eof
)

:eof

pause