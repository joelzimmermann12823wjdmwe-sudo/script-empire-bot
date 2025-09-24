#!/bin/bash
while true; do
    echo "$(date): 🔄 Cloud Shell Reconnect"
    
    # Bot starten
    echo "$(date): 🚀 Starte Bot..."
    python3 bot.py
    
    # Warten und neu verbinden
    echo "$(date): ⏸️  Warte 30 Sekunden..."
    sleep 30
    
    # Cloud Shell reaktivieren
    echo "$(date): 🔌 Versuche Reconnect..."
    curl -s https://shell.cloud.google.com/ > /dev/null 2>&1
done
