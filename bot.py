import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import datetime
import aiohttp
import asyncio
import pytz
from language_system import language_system

# ========== KONFIGURATION ========== #
load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
TEAM_ROLE_IDS = [int(x.strip()) for x in os.getenv('TEAM_ROLE_IDS', '').split(',') if x.strip()]

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='.', intents=intents, help_command=None)

# ========== BEFEHLS SYSTEM ========== #
def is_team_member():
    """Prüft ob der User eine Team-Rolle hat"""
    async def predicate(interaction: discord.Interaction):
        if not interaction.guild:  # DM nicht erlaubt
            return False
        
        user_roles = [role.id for role in interaction.user.roles]
        has_team_role = any(role_id in user_roles for role_id in TEAM_ROLE_IDS)
        
        return has_team_role
    return commands.check(predicate)

def is_admin():
    """Prüft ob der User Administrator ist"""
    async def predicate(interaction: discord.Interaction):
        return interaction.user.guild_permissions.administrator
    return commands.check(predicate)

# ========== WEITERER CODE ========== #
# Globale Bot-Datenbank
class BotData:
    def __init__(self):
        berlin_tz = pytz.timezone('Europe/Berlin')
        self.start_time = datetime.datetime.now(berlin_tz)
        self.stats = {
            "commands_used": 0,
            "last_refresh": datetime.datetime.now(berlin_tz),
            "last_report": datetime.datetime.now(berlin_tz),
            "last_report_hour": -1,
            "online": True,
            "modules_loaded": []
        }
        self.language_system = language_system
        self.timezone = berlin_tz
        self.team_role_ids = TEAM_ROLE_IDS  # Rollen-IDs speichern

bot_data = BotData()

# ========== MODUL SYSTEM ========== #
async def load_all_modules():
    """Lädt automatisch ALLE .py Dateien aus dem commands/ Ordner"""
    commands_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'commands')
    modules_loaded = []
    
    if not os.path.exists(commands_dir):
        os.makedirs(commands_dir)
        print(f'📁 commands/ Ordner erstellt: {commands_dir}')
        return modules_loaded
    
    for filename in os.listdir(commands_dir):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = filename[:-3]
            
            try:
                import importlib.util
                module_path = os.path.join(commands_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, module_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, 'setup'):
                    await module.setup(bot, bot_data, language_system)
                    modules_loaded.append(module_name)
                    print(f'✅ Modul geladen: {module_name}')
                else:
                    print(f'⚠️  {module_name} hat keine setup() Funktion')
                    
            except Exception as e:
                print(f'❌ Fehler beim Laden von {module_name}: {e}')
    
    bot_data.stats['modules_loaded'] = modules_loaded
    return modules_loaded

# ========== AUTO-MONITOR SYSTEM ========== #
@tasks.loop(minutes=5)
async def auto_refresh_commands():
    """Automatisches Command-Refresh alle 5 Minuten"""
    try:
        synced = await bot.tree.sync()
        bot_data.stats['last_refresh'] = datetime.datetime.now(bot_data.timezone)
        bot_data.stats['commands_count'] = len(synced)
        print(f'🔄 {len(synced)} Commands synchronisiert')
    except Exception as e:
        print(f'❌ Auto-Refresh Fehler: {e}')

@tasks.loop(minutes=1)
async def auto_status_report():
    """Sendet Bericht zur vollen Stunde"""
    if not WEBHOOK_URL:
        return
        
    current_time = datetime.datetime.now(bot_data.timezone)
    
    if current_time.minute == 0:
        last_hour = bot_data.stats.get('last_report_hour', -1)
        current_hour = current_time.hour
        
        if last_hour != current_hour:
            try:
                async with aiohttp.ClientSession() as session:
                    uptime = current_time - bot_data.start_time
                    days = uptime.days
                    hours, remainder = divmod(uptime.seconds, 3600)
                    minutes, _ = divmod(remainder, 60)
                    
                    embed = discord.Embed(
                        title="🕐 Stündlicher Bot-Report",
                        description=f"Automatischer Report zur vollen Stunde ({current_time.strftime('%H:%M')} Uhr)",
                        color=discord.Color.blue(),
                        timestamp=current_time
                    )
                    
                    embed.add_field(
                        name="📊 System Status",
                        value=f"**Laufzeit:** {days}T {hours}Std {minutes}Min\n"
                              f"**Module:** {len(bot_data.stats['modules_loaded'])} geladen\n"
                              f"**Commands:** {bot_data.stats.get('commands_count', 0)} aktiv\n"
                              f"**Server:** {len(bot.guilds)}",
                        inline=True
                    )
                    
                    embed.add_field(
                        name="🔄 Letzte Aktivität",
                        value=f"**Refresh:** {bot_data.stats['last_refresh'].strftime('%H:%M:%S')}\n"
                              f"**Commands:** {bot_data.stats['commands_used']} genutzt",
                        inline=True
                    )
                    
                    webhook = discord.Webhook.from_url(WEBHOOK_URL, session=session)
                    await webhook.send(embed=embed, username="Bot Stunden-Report")
                    
                    bot_data.stats['last_report_hour'] = current_hour
                    bot_data.stats['last_report'] = current_time
                    print(f"✅ Stunden-Report gesendet um {current_time.strftime('%H:%M')} Uhr")
                    
            except Exception as e:
                print(f'❌ Auto-Report Fehler: {e}')

# ========== BOT EVENTS ========== #
@bot.event
async def on_ready():
    print(f'🚀 Bot gestartet als {bot.user.name}')
    print(f'🏠 Server: {len(bot.guilds)}')
    print(f'⏰ Zeitzone: Europe/Berlin')
    
    modules = await load_all_modules()
    print(f'📦 {len(modules)} Module geladen')
    
    auto_refresh_commands.start()
    auto_status_report.start()
    
    print('⏰ Auto-System aktiviert: 5min Refresh, Stündlicher Report')
    print('🔧 Bot ist bereit!')

@bot.event
async def on_command_completion(ctx):
    bot_data.stats['commands_used'] += 1

# ========== ERROR HANDLER ========== #
@auto_refresh_commands.error
async def refresh_error(error):
    print(f'❌ Auto-Refresh Fehler: {error}')

@auto_status_report.error
async def report_error(error):
    print(f'❌ Auto-Report Fehler: {error}')

# ========== START SYSTEM ========== #
if __name__ == "__main__":
    if TOKEN:
        print('🔧 Starte Bot-System...')
        bot.run(TOKEN)
    else:
        print('❌ DISCORD_TOKEN nicht in .env gefunden!')