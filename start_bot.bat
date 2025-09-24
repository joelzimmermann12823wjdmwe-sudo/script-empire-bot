@echo off
:start
echo Starte Bot...
python main_bot.py
echo Bot wurde beendet. Neustart in 5 Sekunden...
timeout /t 5
goto start