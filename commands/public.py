import discord

async def setup(bot, bot_data, lang_system):
    @bot.tree.command(
        name="hilfe",
        description="Hilfe für alle User - Zeige verfügbare Commands"
    )
    async def hilfe_command(interaction: discord.Interaction):
        user_roles = [role.id for role in interaction.user.roles] if interaction.guild else []
        is_team = any(role_id in user_roles for role_id in bot_data.team_role_ids) if interaction.guild else False
        is_admin = interaction.user.guild_permissions.administrator if interaction.guild else False
        
        embed = discord.Embed(
            title="❓ Script Empire Bot Hilfe",
            description="Alle verfügbaren Commands für dich:",
            color=0xff0000
        )
        
        # Commands für alle
        public_commands = "• /hilfe - Diese Hilfe\n• /botinfo - Bot Informationen"
        
        # Commands für Team
        team_commands = "\n• /team - Team Bereich" if is_team else ""
        
        # Commands für Admin
        admin_commands = "\n• /admin - Admin Bereich" if is_admin else ""
        
        embed.add_field(
            name="🔹 Commands für dich",
            value=f"{public_commands}{team_commands}{admin_commands}",
            inline=False
        )
        
        embed.add_field(
            name="👤 Deine Berechtigungen",
            value=f"**Team-Mitglied:** {'✅' if is_team else '❌'}\n"
                  f"**Administrator:** {'✅' if is_admin else '❌'}",
            inline=True
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)