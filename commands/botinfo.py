import discord
from datetime import datetime
import pytz

async def setup(bot, bot_data, lang_system):
    @bot.tree.command(
        name=lang_system.get_text("botinfo_name"),
        description=lang_system.get_text("botinfo_description")
    )
    async def botinfo(interaction: discord.Interaction):
        user_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None
        
        # Berlin timezone
        berlin_tz = pytz.timezone('Europe/Berlin')
        current_time = datetime.now(berlin_tz)
        
        # Calculate uptime
        uptime = current_time - bot_data.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Translated time units
        if days > 0:
            uptime_str = f"{days} {lang_system.get_text('days', user_id, guild_id)}, {hours} {lang_system.get_text('hours', user_id, guild_id)}, {minutes} {lang_system.get_text('minutes', user_id, guild_id)}"
        else:
            uptime_str = f"{hours} {lang_system.get_text('hours', user_id, guild_id)}, {minutes} {lang_system.get_text('minutes', user_id, guild_id)}, {seconds} {lang_system.get_text('seconds', user_id, guild_id)}"
        
        # Embed with English as default
        embed = discord.Embed(
            title=lang_system.get_text("botinfo_title", user_id, guild_id),
            description=lang_system.get_text("botinfo_desc", user_id, guild_id),
            color=0x0099ff,
            timestamp=current_time
        )
        
        # Bot Statistics (fully translated)
        embed.add_field(
            name="📊 **" + lang_system.get_text("statistics", user_id, guild_id) + "**",
            value=f"**{lang_system.get_text('online_since', user_id, guild_id)}:** {uptime_str}\n"
                  f"**{lang_system.get_text('active_commands', user_id, guild_id)}:** {bot_data.stats.get('commands_count', 0)}\n"
                  f"**{lang_system.get_text('commands_used', user_id, guild_id)}:** {bot_data.stats.get('commands_used', 0)}\n"
                  f"**{lang_system.get_text('servers', user_id, guild_id)}:** {len(bot.guilds)}",
            inline=True
        )
        
        # System Information
        embed.add_field(
            name="🔄 **" + lang_system.get_text("system_status", user_id, guild_id) + "**",
            value=f"**{lang_system.get_text('modules_loaded', user_id, guild_id)}:** {len(bot_data.stats.get('modules_loaded', []))}\n"
                  f"**🛠️ {lang_system.get_text('last_update', user_id, guild_id)}:** {bot_data.stats.get('last_refresh', current_time).strftime('%d.%m.%Y %H:%M')}\n"
                  f"**📋 {lang_system.get_text('last_report', user_id, guild_id)}:** {bot_data.stats.get('last_report', current_time).strftime('%d.%m.%Y %H:%M')}",
            inline=True
        )
        
        # Bot Features (translated)
        embed.add_field(
            name="✨ **" + lang_system.get_text("features", user_id, guild_id) + "**",
            value=lang_system.get_text("features_text", user_id, guild_id),
            inline=False
        )
        
        # Footer (translated)
        embed.set_footer(text=lang_system.get_text("footer_text", user_id, guild_id))
        
        # Bot Avatar
        if bot.user.avatar:
            embed.set_thumbnail(url=bot.user.avatar.url)
        
        await interaction.response.send_message(embed=embed)
        bot_data.stats["commands_used"] += 1