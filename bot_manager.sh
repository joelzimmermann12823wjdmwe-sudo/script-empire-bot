#!/bin/bash
# Script Empire Bot - 24/7 Manager
BOT_DIR="/home/joelzimmermann12823wjdmwe/script-empire-bot"
LOG_FILE="$BOT_DIR/bot.log"
RESTART_DELAY=5

echo "=== Script Empire Bot 24/7 Manager ==="
echo "Start: $(date)"
echo "Bot Directory: $BOT_DIR"

cd $BOT_DIR

while true; do
    echo "[$(date)] 🚀 Starte Bot..." | tee -a $LOG_FILE
    
    # Bot starten und Output loggen
    python3 bot.py 2>&1 | tee -a $LOG_FILE
    
    EXIT_CODE=${PIPESTATUS[0]}
    echo "[$(date)] ⚠️ Bot beendet mit Code: $EXIT_CODE" | tee -a $LOG_FILE
    echo "[$(date)] 🔄 Neustart in $RESTART_DELAY Sekunden..." | tee -a $LOG_FILE
    
    sleep $RESTART_DELAY
done