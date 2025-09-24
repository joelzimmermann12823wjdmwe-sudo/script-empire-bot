import discord
from datetime import datetime

async def setup(bot, bot_data, lang_system):
    # Command mit automatischer Übersetzung
    @bot.tree.command(
        name=lang_system.get_command_text("info_style", "name", command="stats", topic="statistics"),
        description=lang_system.get_command_text("info_style", "description", command="stats", topic="statistics")
    )
    async def stats(interaction: discord.Interaction):
        user_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None
        
        # Automatisch übersetzte Texte
        title = lang_system.get_command_text("info_style", "title", user_id, guild_id, topic="Statistics")
        stats_title = lang_system.get_command_text("info_style", "statistics", user_id, guild_id, topic="Bot")
        
        embed = discord.Embed(
            title=title,
            color=0x0099ff,
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name=stats_title,
            value=f"**Commands Used:** {bot_data.stats.get('commands_used', 0)}\n"
                  f"**Servers:** {len(bot.guilds)}\n"
                  f"**Uptime:** {(datetime.now() - bot_data.start_time).days} days",
            inline=True
        )
        
        await interaction.response.send_message(embed=embed)
        bot_data.stats["commands_used"] += 1