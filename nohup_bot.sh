#!/bin/bash
# NoHup Fallback
nohup python3 bot.py > bot_nohup.log 2>&1 &
echo "✅ Bot mit NoHup gestartet. PID: $!"
echo "📋 Logs: tail -f bot_nohup.log"
