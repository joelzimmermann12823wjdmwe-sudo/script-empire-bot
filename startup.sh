#!/bin/bash
echo "🚀 Starte Bot automatisch..."
cd /home/joelzimmermann12823wjdmwe/script-empire-bot/  # Pfad anpassen!
nohup ./keepalive.sh > keepalive.log 2>&1 &
echo "✅ Bot Startup fertig"