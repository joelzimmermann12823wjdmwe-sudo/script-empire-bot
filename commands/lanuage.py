import discord

async def setup(bot, bot_data, lang_system):
    @bot.tree.command(
        name=lang_system.get_text("language_name"),
        description=lang_system.get_text("language_description")
    )
    async def language(interaction: discord.Interaction, language: str):
        user_id = interaction.user.id
        guild_id = interaction.guild.id if interaction.guild else None
        
        if language.lower() in ["de", "deutsch", "german"]:
            lang_system.set_user_language(user_id, "de")
            success_msg = "✅ " + lang_system.get_text("language_changed", user_id, guild_id) + " to **German**!"
        elif language.lower() in ["en", "englisch", "english"]:
            lang_system.set_user_language(user_id, "en")
            success_msg = "✅ " + lang_system.get_text("language_changed", user_id, guild_id) + " to **English**!"
        else:
            await interaction.response.send_message(
                lang_system.get_text("language_help", user_id, guild_id),
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title=lang_system.get_text("language_title", user_id, guild_id),
            description=success_msg,
            color=0x00ff00
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)