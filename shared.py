import nextcord
from nextcord.ext import commands
from nextcord.utils import get

async def role_designation(user, user_id, guild, guild_id, channel, level, db_pool):
  async with db_pool.acquire() as cursor:
    role_id = await cursor.fetchval("SELECT role_id FROM level_roles WHERE guild_id = $1 AND level = $2", guild_id, level)
    if role_id:
      role = nextcord.utils.get(guild.roles, id=role_id)
      if role:
        server_roles_ids = await cursor.fetch("SELECT role_id FROM level_roles WHERE guild_id = $1", guild_id)
        server_roles_ids_formatted = []
        user_roles = [role.name for role in user.roles if role.name != "@everyone"]
        server_roles = []
        for id_role in server_roles_ids:
          server_roles_ids_formatted.append(id_role['role_id'])

        for roles in server_roles_ids_formatted:
          role_review = nextcord.utils.get(guild.roles, id=roles)
          if str(role_review) in user_roles:
            await user.remove_roles(role_review)

        await user.add_roles(role) 
        embed = nextcord.Embed(title=f"**__Congratulations!__**",
          description=f"You have been awarded the {role.name} role for reaching level {level}!",
          colour=0x00b0f4)
        embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
        embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
        async with db_pool.acquire() as cursor:
          levelup_channel = await cursor.fetchval("SELECT channel_id FROM level_up_channel WHERE guild_id = $1", guild_id)
        if levelup_channel is None:
          await channel.send(f"{user.mention}", embed=embed)
        else:
          channel_set = get(guild.channels, id=levelup_channel)
          await channel_set.send(f"{user.mention}", embed=embed)