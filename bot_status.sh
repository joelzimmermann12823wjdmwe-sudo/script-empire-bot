#!/bin/bash
# Bot Status Monitor
echo "=== Script Empire Bot Status ==="
echo "Systemzeit: $(date)"

# Prozess Check
echo -n "📊 Bot Prozess: "
if pgrep -f "python3 bot.py" > /dev/null; then
    echo "✅ Laufend"
    ps aux | grep "python3 bot.py" | grep -v grep
else
    echo "❌ Gestoppt"
fi

# Log Check
echo "📋 Letzte Logs:"
tail -5 bot.log 2>/dev/null || echo "Keine Logs gefunden"

# Systemd Status
if systemctl is-active script-empire-bot > /dev/null 2>&1; then
    echo "🔧 Systemd Service: ✅ Aktiv"
else
    echo "🔧 Systemd Service: ❌ Inaktiv"
fi

# Screen Status
if screen -list | grep -q "script-empire-bot"; then
    echo "💻 Screen Session: ✅ Aktiv"
else
    echo "💻 Screen Session: ❌ Inaktiv"
fi
