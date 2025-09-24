#!/bin/bash
echo "🤖 Bot Status Check..."

# Bessere Prozess-Suche
BOT_PID=$(pgrep -f "python3 bot.py" | head -1)

if [ ! -z "$BOT_PID" ]; then
    echo "✅ Bot läuft (PID: $BOT_PID)"
    echo "📊 Laufzeit: $(ps -p $BOT_PID -o etime= 2>/dev/null || echo 'Unbekannt')"
else
    echo "❌ Bot ist nicht aktiv"
    
    # Prüfe KeepAlive
    KEEPALIVE_PID=$(pgrep -f "keepalive.sh")
    if [ ! -z "$KEEPALIVE_PID" ]; then
        echo "🔧 KeepAlive läuft (PID: $KEEPALIVE_PID)"
    fi
fi