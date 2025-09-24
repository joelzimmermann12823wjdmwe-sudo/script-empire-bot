#!/bin/bash
echo "🤖 Bot KeepAlive Script gestartet..."

while true; do
    # Prüfe ob Botprozess noch läuft
    if ! pgrep -f "python3 bot.py" > /dev/null; then
        echo "$(date): ❌ Bot ist down - starte neu..."
        nohup python3 bot.py > bot.log 2>&1 &
        echo "$(date): ✅ Bot neu gestartet"
    else
        echo "$(date): ✅ Bot läuft stabil"
    fi
    
    # Warte 1 Minute bis zur nächsten Prüfung
    sleep 60
done