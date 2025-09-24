#!/bin/bash
# Screen Session Manager
SESSION_NAME="script-empire-bot"

if screen -list | grep -q "$SESSION_NAME"; then
    echo "✅ Bot läuft bereits in Screen: $SESSION_NAME"
    screen -r $SESSION_NAME
else
    echo "🚀 Starte neuen Screen: $SESSION_NAME"
    screen -S $SESSION_NAME -dm python3 bot.py
    echo "✅ Bot gestartet. Verbinde mit: screen -r $SESSION_NAME"
fi
