"""Resources:
Multiline comments:
https://www.geeksforgeeks.org/multiline-comments-in-python
Initialzing Discord Bot From Replit's article:
https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
https://www.youtube.com/playlist?list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP

Database Resources:
https://datacarpentry.org/python-ecology-lesson/instructor/09-working-with-sql.html, https://www.w3schools.com/sql/sql_select.aspm, https://www.w3schools.com/sql/sql_where.asp, and https://www.w3schools.com/sql/sql_insert.asp
https://www.w3schools.com/sql/sql_delete.asp
https://www.w3schools.com/sql/sql_update.asp
https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
"""

# https://infosecwriteups.com/running-discord-bots-24-7-for-free-with-replit-and-uptime-robot-43caebb0cb60 <----- IMPORTANT


# Database connect along with cursor method and database commit method all throughout main.py from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik

import os
import requests
from pprint import pprint
from nextcord import Interaction # from https://www.youtube.com/watch?v=zvVziW2qS-0&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=17&t=558s&ab_channel=JamesS
import nextcord # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
import asyncio # from https://docs.python.org/3/library/asyncio.html
import asyncpg
from nextcord.application_command import ClientCog, SlashOption # from https://www.youtube.com/watch?v=gtSbqUJLpvM&t=238s&ab_channel=Civo
from nextcord.embeds import Embed # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import commands # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext.commands import context    #from https://docs.replit.com/tutorialsb/python/build-basic-discord-bot- python and # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import tasks, commands
from nextcord.ext.commands import has_permissions, MissingPermissions
from nextcord.ui import View, Button
import about_archer
import about_knight
import about_mage
import help_page
from nextcord.utils import get
import pick_move
import help_pageTWO
import help_pageTHREE
import help_pageFOUR
import help_pageFIVE
import about_battling
import about_levelling
import start_page
import battle_command
from randGIF import randgif
import random
from random import randint
import logging
import signal

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())   #from https://youtu.be/ksAtGCFxrP8#si=A89Nokdcqfsy_tGZ
client.remove_command('help') # Removing the built in help command 

db_pool = None
keep_db_alive_task = None

run = "Main" 

async def create_db_pool():
  # Function to establish database connection using asyncpg
  if run == "Main":
    global db_pool
    DATABASE_HOST = os.environ['DBHOST']
    DATABASE_PORT = os.environ['DBPORT']
    DATABASE_USER = os.environ['DBUSER']
    DATABASE_PASSWORD = os.environ['DBPASSWORD']
    DATABASE_NAME = os.environ['DBNAME']
    try:
      db_pool = await asyncpg.create_pool(
        host = DATABASE_HOST,
        port = DATABASE_PORT,
        user = DATABASE_USER,
        password = DATABASE_PASSWORD,
        database = DATABASE_NAME,
        statement_cache_size=0 
      )
    except Exception as e:
      logging.error(f"Error creating database connection pool: {e}")
  elif run == "Alpha":
    DATABASE_HOST = os.environ['ALPHA_HOST']
    DATABASE_PORT = os.environ['ALPHA_PORT']
    DATABASE_USER = os.environ['ALPHA_USER']
    DATABASE_PASSWORD = os.environ['ALPHA_PASSWORD']
    DATABASE_NAME = os.environ['ALPHA_DBNAME']
    try:
      db_pool = await asyncpg.create_pool(
        host = DATABASE_HOST,
        port = DATABASE_PORT,
        user = DATABASE_USER,
        password = DATABASE_PASSWORD,
        database = DATABASE_NAME,
        statement_cache_size=0 
      )
    except Exception as e:
      logging.error(f"Error creating database connection pool: {e}")

async def ensure_db_pool(pool_conn):
  if pool_conn is None or pool_conn._closed:
      logging.warning("Recreating the database pool (ensure_db_pool).")
      await create_db_pool()
  client.db_pool = db_pool

@tasks.loop(minutes=1)
async def keep_db_alive():
    global db_pool
    try:
      if not keep_db_alive.is_running():
         keep_db_alive.start()
         keep_db_alive_task = keep_db_alive

      if db_pool is None or db_pool._closed:
          logging.warning("Database pool is not initialized (keep_db_alive).")
          await ensure_db_pool(db_pool)

      if "Leveling" not in client.cogs:
          client.db_pool = db_pool
          client.load_extension("cogs.levels")

      async with db_pool.acquire() as cursor:
          try:
              await cursor.execute('SELECT 1')
              logging.info("Executed keep-alive query successfully.")
          except Exception as e:
              logging.error(f"Keep-alive query failed: {e}")
    except Exception as e:
      logging.error(f"Error in keep_db_alive: {e}")

@client.event
async def on_ready(): # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
    logging.info("Bot is up and ready.") #prints when bot is online from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python 
    await create_db_pool()
    client.db_pool = db_pool
    client.load_extension("cogs.levels")
    async with db_pool.acquire() as cursor:
      await cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id BIGINT, guild_id BIGINT, class INTEGER, start INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS battles(battle INTEGER, starter_id BIGINT, starter_hp INTEGER, reciever_id BIGINT, reciever_hp INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS moves(user_id BIGINT, opponent_id BIGINT, move_used TEXT, turn_num INTEGER)')
      await cursor.execute('CREATE TABLE IF NOT EXISTS cooldowns(user_id BIGINT, opponent_id BIGINT, weak TEXT, w_cooldown INTEGER, normal TEXT, n_cooldown INTEGER, special TEXT, s_cooldown INTEGER, avalon_blessing TEXT, ab_cooldown INTEGER)')
      await cursor.execute("""CREATE TABLE IF NOT EXISTS global_levels(user_id BIGINT, exp INTEGER, level INTEGER, exp_needed INTEGER)""")
      await cursor.execute("""CREATE TABLE IF NOT EXISTS server_levels(user_id BIGINT, guild_id BIGINT, exp INTEGER, level INTEGER, exp_needed INTEGER)""")
      await cursor.execute("""CREATE TABLE IF NOT EXISTS level_roles(guild_id BIGINT, level INTEGER, role_id BIGINT)""")
      await cursor.execute("""CREATE TABLE IF NOT EXISTS no_exp_roles(guild_id BIGINT, role_id BIGINT)""")
      await cursor.execute("""CREATE TABLE IF NOT EXISTS no_exp_channels(guild_id BIGINT, channel_id BIGINT)""")
      await cursor.execute("""CREATE TABLE IF NOT EXISTS exp_boosted_roles(guild_id BIGINT, role_id BIGINT, boost_percent INT)""")

    if not keep_db_alive.is_running():
       keep_db_alive.start()
       keep_db_alive_task = keep_db_alive

    logging.info(f"{len(client.guilds)}")
    for i in range(len(client.guilds)):
       logging.info(f"{client.guilds[i].name}")
       logging.info(f"{client.guilds[i].member_count}")  

@client.event
async def on_resumed():
      logging.info("Bot has reconnected to Discord.") 
      global db_pool
      await create_db_pool()
      client.db_pool = db_pool
      client.load_extension('cogs.levels')
      if not keep_db_alive.is_running():
         keep_db_alive.start()
         keep_db_alive_task = keep_db_alive

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return

async def close_pool():
  global db_pool
  global keep_db_alive_task
  if db_pool is not None:
    logging.info("Closing connection pools...")
    await db_pool.close()
    db_pool = None 
  else:
    logging.info("No connection pools to close.")

async def shutdown():
  global keep_db_alive_task
  logging.info("Shutting down gracefully...")
  if keep_db_alive_task is not None:
      keep_db_alive_task.cancel()
      logging.info("Keep alive task cancelled...")
      try:
          await keep_db_alive_task
      except asyncio.CancelledError:
          pass

def handle_shutdowns():
  logging.info("Handling shutdown...")
  signals = (signal.SIGINT, signal.SIGTERM)
  for s in signals:
      logging.info(f"Handling {s}")
      client.loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown()))

@client.command()
async def shutdown(ctx):
  try:
    await ctx.message.delete()
  except nextcord.errors.Forbidden:
    logging.info("User does not have permissions to access command.")
    return
  id = int(os.environ['ID'])
  file = os.environ['FILE']
  guild = int(os.environ['ID_GUILD'])
  if ctx.author.id == id and ctx.guild.id == guild:
      logging.info("Starting closure...")
      await client.http.close()
      await client.close()
      logging.info("Bot shut down...")
  else:
      logging.info("User does not have permissions to access command.")

class PaginationViewLeaderboard(View):
  def __init__(self, embeds, interaction_id):
      super().__init__(timeout=300)
      self.embeds = embeds
      self.current = 0
      self.command_user = interaction_id

  @nextcord.ui.button(label='Previous', style=nextcord.ButtonStyle.grey)
  async def previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      if self.command_user != interaction.user.id:
        await interaction.response.send_message("You cannot modify another user's embed! Use the command yourself to modify your own embed.", ephemeral=True)
      elif self.current > 0:
          self.current -= 1
          await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
      else:
          await interaction.response.defer()

  @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.grey)
  async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      if self.command_user != interaction.user.id:
        await interaction.response.send_message("You cannot modify another user's embed! Use the command yourself to modify your own embed.", ephemeral=True)
      elif self.current < len(self.embeds) - 1:
          self.current += 1
          await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
      else:
          await interaction.response.defer()

@client.slash_command(name='leaderboard', description="View the rankings of people's server levels and server XP on this server!")
async def leaderboard(interaction: Interaction):
    await interaction.response.defer()
    await ensure_db_pool(db_pool)
    async with db_pool.acquire() as cursor:
        data = await cursor.fetch(f"""
            SELECT user_id, level, exp, exp_needed
            FROM server_levels
            WHERE guild_id = $1
            ORDER BY level DESC, exp DESC
        """, interaction.guild_id)

    if not data:
        await interaction.followup.send("No data available for the leaderboard.")
        return

    user_rank = 0
    per_page = 10
    embeds = []
    for i in range(0, len(data), per_page):
        embed = nextcord.Embed(title=f"{interaction.guild} Server Leaderboard", color=nextcord.Color.blue())
        for j, record in enumerate(data[i:i+per_page], start=i+1):
            user = interaction.guild.get_member(record['user_id'])
            if user == interaction.user:
              user_rank = j
            embed.add_field(name=f"{j}. {user}", value=f"Level: {record['level']} | XP: {record['exp']}/{record['exp_needed']}", inline=False)
        embed.set_footer(text=f"Page {len(embeds) + 1}/{(len(data) // per_page) + 1} | Your Rank: {user_rank}")
        embeds.append(embed)
    view = PaginationViewLeaderboard(embeds, interaction.user.id)
    await interaction.followup.send(embed=embeds[0], view=view)

@client.slash_command(name = "assign_level_role", description = "Assign a role that is awarded when a particular server level is reached on this server.")
async def rolelvl(interaction: Interaction, level: int, role: nextcord.Role):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()

  if level < 1:
    await interaction.followup.send("`You cannot assign a role to a level that is less than 1!`")
    return

  async with db_pool.acquire() as cursor:
    level_result = await cursor.fetchval("SELECT role_id FROM level_roles WHERE guild_id = $1 AND level = $2", interaction.guild_id, level)
    role_result = await cursor.fetchval("SELECT level FROM level_roles WHERE guild_id = $1 AND role_id = $2", interaction.guild_id, role.id)

    if level_result is not None or role_result is not None:
      if level_result is not None:
        await interaction.followup.send(f"`Cannot assign level {level} to a role when it has already been assigned to one!`")

      if role_result is not None:
         await interaction.followup.send(f"`Cannot assign role {role} to a level when it has already been assigned to one!`")
      return

  async with db_pool.acquire() as cursor:
    await cursor.execute('INSERT INTO level_roles (guild_id, level, role_id) VALUES ($1, $2, $3)', interaction.guild_id, level, role.id)

  await interaction.followup.send(f"`Successfully set {role.name} for level {level}.`")

@client.slash_command(name = "remove_level_role", description = "Remove a role that is awarded when a particular server level is reached on this server.")
async def removelvl(interaction: Interaction, level: int):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  async with db_pool.acquire() as cursor:
    level_result = await cursor.fetchval('SELECT role_id FROM level_roles WHERE guild_id = $1 AND level = $2', interaction.guild_id, level)

  if level_result is None:
    await interaction.response.send_message("`Cannot delete level role that doesn't exist in the database!`")
  else:
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
       await cursor.execute('DELETE FROM level_roles WHERE level = $1 AND guild_id = $2', level, interaction.guild_id)

    await interaction.followup.send(f"`Successfully deleted role for level {level}.`")

@client.slash_command(name = "clear_level_roles", description = "Clear all the server levels associated with their respective role on this server.")
async def clearlvl(interaction: Interaction):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    level_roles_result = await cursor.fetch("SELECT * FROM level_roles WHERE guild_id = $1", interaction.guild_id)
    if level_roles_result == []:
       await interaction.followup.send("`Cannot reset roles that don't exist!`")
       return
    await cursor.execute('DELETE FROM level_roles WHERE guild_id = $1', interaction.guild_id)
    await interaction.followup.send(f"`Successfully reset all level roles on the server.`")

@client.slash_command(name = "see_level_roles", description = "See the roles awarded when reaching a particular server level on this server!")
async def seelvlroles(interaction: Interaction):
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    role_levels = await cursor.fetch("SELECT level, role_id FROM level_roles WHERE guild_id = $1", interaction.guild_id)

  role_levels_formatted = []

  for record in role_levels:
    role_levels_formatted.append([record['role_id'], record['level']])

  role_levels_formatted.sort(key=lambda x: x[1])

  i = 0
  embed_description = ""
  if role_levels == []:
    embed_description = "No level roles to show."
  else:
    while i < len(role_levels_formatted):
      role = nextcord.utils.get(interaction.guild.roles, id=role_levels_formatted[i][0])
      embed_description = embed_description + "Level " + str(role_levels_formatted[i][1]) + ": " + str(role.mention) + "\n"
      i += 1

  embed = nextcord.Embed(
    title=f"Level Roles for {interaction.guild}",
    description=embed_description,
    color=nextcord.Color.blue()
)
  await interaction.followup.send(embed=embed)

@client.slash_command(name = "assign_no_exp_role", description = "Assign a role that cannot gain server XP from battling or messaging on this server.")
async def assignnoexp(interaction: Interaction, role: nextcord.Role):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    role_result = await cursor.fetchval("SELECT role_id FROM no_exp_roles WHERE guild_id = $1 AND role_id = $2", interaction.guild_id, role.id)

    if role_result is not None:
      await interaction.followup.send(f"`That role has already been assigned to not earn any XP.`")
      return

  async with db_pool.acquire() as cursor:
    boosted_xp_result = await cursor.fetchval(f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {role.id}")

    if boosted_xp_result is not None:
      await interaction.followup.send(f"`Cannot assign **{role}** to be a no XP role when it is already a boosted XP role!`")
      return

  async with db_pool.acquire() as cursor:
    await cursor.execute('INSERT INTO no_exp_roles (guild_id, role_id) VALUES ($1, $2)', interaction.guild_id, role.id)

  await interaction.followup.send(f"`Successfully set {role.name} to not earn any XP on the server.`")

@client.slash_command(name = "remove_no_exp_role", description = "Remove a role that cannot gain server XP from battling or messaging on this server.")
async def removenoexp(interaction: Interaction, role: nextcord.Role):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  async with db_pool.acquire() as cursor:
    role_result = await cursor.fetchval('SELECT role_id FROM no_exp_roles WHERE guild_id = $1 AND role_id = $2', interaction.guild_id, role.id)

  if role_result is None:
    await interaction.response.send_message("`Cannot delete a no exp role that doesn't exist in the database!`")
  else:
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
       await cursor.execute('DELETE FROM no_exp_roles WHERE role_id = $1 AND guild_id = $2', role.id, interaction.guild_id)

    await interaction.followup.send(f"`{role} can now gain XP again on the server.`")


@client.slash_command(name = "clear_no_exp_roles", description = "Remove the no XP restriction from all roles that have it on this server.")
async def clearnoexp(interaction: Interaction):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    no_exp_result = await cursor.fetch("SELECT * FROM no_exp_roles WHERE guild_id = $1", interaction.guild_id)
    if no_exp_result == []:
       await interaction.followup.send("`Cannot reset roles that don't exist!`")
       return
    await cursor.execute('DELETE FROM no_exp_roles WHERE guild_id = $1', interaction.guild_id)
    await interaction.followup.send(f"`Successfully reset all no exp roles on the server.`")

@client.slash_command(name = "see_no_exp_roles", description = "See the roles on this server that cannot gain server XP from battling or messaging.")
async def seelvlroles(interaction: Interaction):
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    roles_no_exp = await cursor.fetch("SELECT role_id FROM no_exp_roles WHERE guild_id = $1", interaction.guild_id)

  role_no_exp_formatted = []

  for record in roles_no_exp:
    role_no_exp_formatted.append(record['role_id'])

  embed_description = ""
  if role_no_exp_formatted == []:
    embed_description = "All roles can earn XP on the server."
  else:
    for id in role_no_exp_formatted:
      role = nextcord.utils.get(interaction.guild.roles, id=id)
      embed_description = embed_description + str(role.mention) + "\n"

  embed = nextcord.Embed(
    title=f"No XP Roles for {interaction.guild}",
    description=embed_description,
    color=nextcord.Color.blue()
)
  await interaction.followup.send(embed=embed)

@client.slash_command(name = "assign_no_exp_channel", description = "Assign a channel on this server where server XP cannot be earned from messaging (not battling).")
async def assignnochannel(interaction: Interaction, channel: nextcord.TextChannel):
  if not interaction.user.guild_permissions.manage_channels:
    await interaction.response.send_message("You need the Manage Channels permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    channel_result = await cursor.fetchval("SELECT channel_id FROM no_exp_channels WHERE guild_id = $1 AND channel_id = $2", interaction.guild_id, channel.id)

    if channel_result is not None:
      await interaction.followup.send(f"`That channel has already been assigned to not earn any XP in it.`")
      return

  async with db_pool.acquire() as cursor:
    await cursor.execute('INSERT INTO no_exp_channels (guild_id, channel_id) VALUES ($1, $2)', interaction.guild_id, channel.id)

  await interaction.followup.send(f"`Successfully set {channel.name} to be a channel where users cannot earn any XP.`")

@client.slash_command(name = "remove_no_exp_channel", description = "Remove a channel on this server where server XP cannot be gained from messaging (not battling).")
async def removenochannel(interaction: Interaction, channel: nextcord.TextChannel):
  if not interaction.user.guild_permissions.manage_channels:
    await interaction.response.send_message("You need the Manage Channels permission to use this command, which you don't have.", ephemeral=True)
    return
  async with db_pool.acquire() as cursor:
    channel_result = await cursor.fetchval('SELECT channel_id FROM no_exp_channels WHERE guild_id = $1 AND channel_id = $2', interaction.guild_id, channel.id)

  if channel_result is None:
    await interaction.response.send_message("`Cannot delete a no XP channel that doesn't exist in the database!`")
  else:
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
       await cursor.execute('DELETE FROM no_exp_channels WHERE channel_id = $1 AND guild_id = $2', channel.id, interaction.guild_id)

    await interaction.followup.send(f"`Users can now gain XP in the {channel} channel again.`")


@client.slash_command(name = "clear_no_exp_channels", description = "Remove the no server XP restriction from all the channels that have it on this server.")
async def clearnoexpchannel(interaction: Interaction):
  if not interaction.user.guild_permissions.manage_channels:
    await interaction.response.send_message("You need the Manage Channels permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    no_exp_channel = await cursor.fetch("SELECT * FROM no_exp_channels WHERE guild_id = $1", interaction.guild_id)
    if no_exp_channel == []:
       await interaction.followup.send("`Cannot reset channels when none exist in the database!`")
       return
    await cursor.execute('DELETE FROM no_exp_channels WHERE guild_id = $1', interaction.guild_id)
    await interaction.followup.send(f"`Successfully reset all no XP channels on the server.`")

@client.slash_command(name = "see_no_exp_channels", description = "See the channels where messaging (not battling) will not award you any server XP.")
async def seechannelroles(interaction: Interaction):
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    channels_no_exp = await cursor.fetch("SELECT channel_id FROM no_exp_channels WHERE guild_id = $1", interaction.guild_id)

  channel_no_exp_formatted = []

  for record in channels_no_exp:
    channel_no_exp_formatted.append(record['channel_id'])

  embed_description = ""
  if channel_no_exp_formatted == []:
    embed_description = "Users can gain XP on all channels in the server."
  else:
    for id in channel_no_exp_formatted:
      channel = get(interaction.guild.channels, id=id)
      embed_description = embed_description + str(channel.mention) + "\n"

  embed = nextcord.Embed(
    title=f"No XP Channels for {interaction.guild}",
    description=embed_description,
    color=nextcord.Color.blue()
)
  await interaction.followup.send(embed=embed)

# EXP BOOST ROLE COMMANDS BELOW

@client.slash_command(name = "assign_exp_boosted_role", description = "Assign a role that gains extra server XP on this server from messaging (not battling).")
async def assignextraexp(interaction: Interaction, role: nextcord.Role, boost_percent: int):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()

  async with db_pool.acquire() as cursor:
    role_result = await cursor.fetchval("SELECT role_id FROM exp_boosted_roles WHERE guild_id = $1 AND role_id = $2", interaction.guild_id, role.id)

    if role_result is not None:
      await interaction.followup.send(f"`That role has already been assigned to earn extra XP.`")
      return

  async with db_pool.acquire() as cursor:
    no_xp_result = await cursor.fetchval(f"SELECT guild_id FROM no_exp_roles WHERE role_id = {role.id}")

    if no_xp_result is not None:
      await interaction.followup.send(f"`Cannot assign **{role}** to be a boosted XP role when it is already a no XP role!`")
      return

  if boost_percent > 200:
    await interaction.followup.send("`Your boost percent cannot be bigger than 200%.`")
    return
  elif boost_percent < 1:
    await interaction.followup.send("`Your boost percent cannot be smaller than 1%.`")
    return

  async with db_pool.acquire() as cursor:
    await cursor.execute('INSERT INTO exp_boosted_roles (guild_id, role_id, boost_percent) VALUES ($1, $2, $3)', interaction.guild_id, role.id, boost_percent)

  await interaction.followup.send(f"`Successfully set {role.name} to earn {boost_percent}% more XP on the server.`")

@client.slash_command(name = "remove_exp_boosted_role", description = "Remove a role that gains extra server XP from messaging (not battling) on this server.")
async def removeextraexp(interaction: Interaction, role: nextcord.Role):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  async with db_pool.acquire() as cursor:
    role_result = await cursor.fetchval('SELECT role_id FROM exp_boosted_roles WHERE guild_id = $1 AND role_id = $2', interaction.guild_id, role.id)

  if role_result is None:
    await interaction.response.send_message("`Cannot delete a boosted XP role that doesn't exist in the database!`")
  else:
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
       boost_val = await cursor.fetchval(f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {role.id} AND guild_id = {interaction.guild_id}")
       await cursor.execute('DELETE FROM exp_boosted_roles WHERE role_id = $1 AND guild_id = $2', role.id, interaction.guild_id)

    await interaction.followup.send(f"`Removed {boost_val}% XP boost from the {role} role.`")

@client.slash_command(name = "clear_exp_boosted_roles", description = "Clear all the server XP boosts from the applicable roles on this server.")
async def clearextraexp(interaction: Interaction):
  if not interaction.user.guild_permissions.manage_roles:
    await interaction.response.send_message("You need the Manage Roles permission to use this command, which you don't have.", ephemeral=True)
    return
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    boosted_exp_result = await cursor.fetch("SELECT * FROM exp_boosted_roles WHERE guild_id = $1", interaction.guild_id)
    if boosted_exp_result == []:
       await interaction.followup.send("`Cannot reset roles that don't exist!`")
       return
    await cursor.execute('DELETE FROM exp_boosted_roles WHERE guild_id = $1', interaction.guild_id)
    await interaction.followup.send(f"`Successfully reset all XP boosted roles on the server.`")

@client.slash_command(name = "see_exp_boosted_roles", description = "See the roles that gain extra server XP when messaging on this server along with their % boost!")
async def seeextraxp(interaction: Interaction):
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:
    roles_boosted_exp = await cursor.fetch("SELECT role_id, boost_percent FROM exp_boosted_roles WHERE guild_id = $1", interaction.guild_id)

  role_boosted_exp_formatted = []

  for record in roles_boosted_exp:
     role_boosted_exp_formatted.append([record['role_id'], record['boost_percent']])

  role_boosted_exp_formatted.sort(key=lambda x: x[1], reverse=True)

  i = 0
  embed_description = ""
  if role_boosted_exp_formatted == []:
    embed_description = "No boosted XP roles to show."
  else:
    while i < len(role_boosted_exp_formatted):
      role = nextcord.utils.get(interaction.guild.roles, id=role_boosted_exp_formatted[i][0])
      embed_description = embed_description + str(role.mention) + ": " + f"{role_boosted_exp_formatted[i][1]}%" "\n"
      i += 1

  embed = nextcord.Embed(
    title=f"Boosted XP Roles for {interaction.guild}",
    description=embed_description,
    color=nextcord.Color.blue()
)
  await interaction.followup.send(embed=embed)


@client.slash_command(name = "playercount", description = "See how many users are registered with the bot!")
async def count(interaction: Interaction):
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:
      user_data = await cursor.fetch('SELECT start FROM users')
      class_data = await cursor.fetch('SELECT class FROM users')
      user_count = 0 
      if user_data != None: 
        for data in user_data:
          user_count += 1

      class_count = 0
      if class_data != None: 
        for data in class_data:
          if data['class'] in [1, 2, 3]:
            class_count += 1
      await interaction.followup.send(f"User Count: **__{user_count}__**\n \n Users that Picked a Class: **__{class_count}__** \n \n **__Summary__**: \n \n **__{user_count}__** player(s) have used `/start` and **__{class_count}__** of them have picked a class!")

@client.slash_command(name = "gif", description = "Generate a GIF! Idek why we have this feature its just there.") 
async def gif(interaction: Interaction, query: str = SlashOption(description="Search for the GIF that you want to generate!")): #prefix command to grab gif based on arg
  await interaction.response.defer()
  media_filter = "gif, tinygif"
  random = True
  SECRET_KEY = os.environ["TENOR_API_KEY"]
  ckey = "my_client_key"
  lim = 1

  try:
    r = requests.get(
      f"https://tenor.googleapis.com/v2/search?q={query}&key={SECRET_KEY}&client_key={ckey}&limit={lim}&media_filter={media_filter}&random={random}") #requests api for an obj containing our results
    r.raise_for_status()
  except requests.exceptions.RequestException as e:
    await interaction.followup.send("Error fetching GIF. Please try again later.")
    return

  if r.status_code == 200:
    data = r.json()
    url = data['results'][0]['media_formats']['gif']['url'] #opens the json obj and grabs the gif url
    embed = Embed(title="The GIF Machine", 
                  description=f"Here's your GIF! {interaction.user.mention}", 
                  color=0x00ff00)
    embed.set_image(url=f"{url}")
    embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/qY14QUB9KPYAAAAi/tenor-stickers.gif")
    await interaction.response.send_message(embed=embed) #sends the gif and deletes the user msg to not clutter the chat
  else:
    embed = Embed(title="No Results Found")
    await interaction.response.send_message(embed=embed)

# Define a class for the pagination view
class PaginationView(View):
    def __init__(self, embeds, page, interaction_id):
        super().__init__(timeout=600)
        self.embeds = embeds
        self.current = page
        self.command_user = interaction_id

    @nextcord.ui.button(label='Prev', style=nextcord.ButtonStyle.grey)
    async def previous(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.command_user != interaction.user.id:
          await interaction.response.send_message("You cannot modify another user's embed! Use the command yourself to modify your own embed.", ephemeral=True)
        elif self.current > 0:
            self.current -= 1
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
        else:
            await interaction.response.defer()

    @nextcord.ui.button(label='Next', style=nextcord.ButtonStyle.grey)
    async def next(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.command_user != interaction.user.id:
          await interaction.response.send_message("You cannot modify another user's embed! Use the command yourself to modify your own embed.", ephemeral=True)
        elif self.current < len(self.embeds) - 1:
            self.current += 1
            await interaction.response.edit_message(embed=self.embeds[self.current], view=self)
        else:
            await interaction.response.defer()

@client.slash_command(name = "help", description = "Are you confused?") #slash command to print out help pages
async def help(interaction: Interaction, page: int = SlashOption(name="page", choices={"#1": 1, "#2": 2, "#3": 3, "#4": 4, "#5": 5})):
    await interaction.response.defer()
    botName = client.user.name
    bot_avatar_url = client.user.avatar.url
    embed_pgone = await help_page.help(interaction, botName, bot_avatar_url)
    embed_pgtwo = await help_pageTWO.help(interaction, botName, bot_avatar_url)
    embed_pgthree = await help_pageTHREE.help(interaction, botName, bot_avatar_url)
    embed_pgfour = await help_pageFOUR.help(interaction, botName, bot_avatar_url)
    embed_pgfive = await help_pageFIVE.help(interaction, botName, bot_avatar_url)
    help_pages = [embed_pgone, embed_pgtwo, embed_pgthree,  embed_pgfour, embed_pgfive]
    view = PaginationView(help_pages, page-1, interaction.user.id)
    await interaction.followup.send(embed=help_pages[page-1], view=view)

@client.slash_command(name = "avi_manual", description = "Learn a little more about Avalon Index and its specific classes!")
async def about(interaction: Interaction, page: int = SlashOption(name = "page", choices = {"Battling": 1, "Levelling": 2, "Knight": 3, "Archer": 4, "Mage": 5})):
        await interaction.response.defer()
        bot_name = client.user.name
        bot_avatar_url = client.user.avatar.url
        ab_levelling = await (about_levelling.about(interaction, bot_name, bot_avatar_url))
        ab_battling = await (about_battling.about(interaction, bot_name, bot_avatar_url))
        ab_knight = await (about_knight.about(interaction, bot_name, bot_avatar_url))
        ab_archer = await (about_archer.about(interaction, bot_name, bot_avatar_url))
        ab_mage = await (about_mage.about(interaction, bot_name, bot_avatar_url))
        ab_pages = [ab_battling, ab_levelling, ab_knight, ab_archer, ab_mage]
        view = PaginationView(ab_pages, page-1, interaction.user.id)
        await interaction.followup.send(embed=ab_pages[page-1], view=view)

# The start command essentially starts the game for the user that uses the command and allows them to use commands such as stats, battle, pick, and so on. It does this by creating a new section in the users table and setting the start value column to one. Additionally, the other functions rely on this value by checking if the start value is one, or in other words if the user used the start command, if the user did not use the command, the user won't be able to use the other functions. Additionally, if the user already used start, the command will not work by checking the start value. The command also sends an embed explaining the game and hot to get started.
# Start command implementation code from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik

@client.slash_command(name = "start", description = "Starts the game!")
async def start(interaction: Interaction): 
  await interaction.response.defer()
  global db_pool
  botName = client.user.name
  bot_avatar_url = client.user.avatar.url

  start_value, check_battle_one, check_battle_two, user_count = await start_page.check_assign(interaction, db_pool)

  if check_battle_one == 1 or check_battle_two == 1 or check_battle_one == 0 or check_battle_two == 0:
      await interaction.followup.send("Cannot start the game when you're in a battle or are requesting/being requested for one! Wait until the battle ends or forfeit the battle when possible! Or just make a move my guy (if it's your turn in the battle)...")
  elif start_value == 1:
      await interaction.followup.send("You have already used /start! If you would like to reset your stats, please use the /reset command.")
  else:
    async with db_pool.acquire() as cursor:

      await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES ($1, $2, $3)', interaction.user.id, interaction.guild_id, 1)

    await start_page.start(interaction, botName, bot_avatar_url, db_pool)

class ConfirmDeny(nextcord.ui.View):
  def __init__(self, interaction_id):
    super().__init__(timeout=30)
    self.interaction_id = interaction_id
    self.value = None

# The function below creates the "yes" button for the reset function, which is red is color, and what it does is it deletes the row in the table of the user that used /reset, resetting their stats and allowing them to use /reset again. Additinally, after the button is pressed, it cannot be pressed again, as the buttons stop working.
  @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green)
  async def y(self, button: nextcord.ui.Button, interaction: Interaction):
      if interaction.user.id != self.interaction_id:
          await interaction.response.send_message("You can't reset stats that aren't yours!", ephemeral=True)
      else:
        await interaction.response.defer()
        async with db_pool.acquire() as cursor:

          await cursor.execute('DELETE FROM users WHERE user_id = $1', interaction.user.id)
          await cursor.execute('DELETE FROM global_levels WHERE user_id = $1', interaction.user.id)

        await interaction.followup.send('Stats successfully deleted. You may use /start to get started again!', ephemeral=True) # Ephermeral makes the message only visible to the user that used the command.
        self.value = True
        self.stop()

# The function below creates the "no" button for the reset function, which is red in color. It merely cancels the command by responding to the interaction by sending a message that says the request was cancelled.
  @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red)
  async def n(self, button: nextcord.ui.Button, interaction: Interaction):
    if interaction.user.id != self.interaction_id:
        await interaction.response.send_message("You can't reset stats that aren't yours!", ephemeral=True)
    else:
      await interaction.response.send_message('Request cancelled.', ephemeral=True)
      self.value = False
      self.stop()

# The reset function below implements the ConfirmDeny class created above and ensures to wait for the user to press a button and eventually times out. Additionally, the function checks that start value is one in the users table so that stats can actually be deleted.
@client.slash_command(name = "reset", description = "Reset your stats and start from scratch!")
async def re(interaction: Interaction):
  await interaction.response.defer()
  view = ConfirmDeny(interaction.user.id)
  async with db_pool.acquire() as cursor:

    battle_check_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    battle_check_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    if battle_check_one == 1 or battle_check_two == 1 or battle_check_one == 0 or battle_check_two == 0:
        await interaction.follouwp.send("You cannot use /reset during battle! Wait until the battle ends or forfeit the battle when possible!", ephemeral=True)
    else:
        start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)
        if start_value == 1:
            await interaction.followup.send("Hold up! Once you reset your stats, you cannot go back, are you sure you want to proceed?", view=view, ephemeral=True)
            await view.wait()
            if view.value is None:
              await interaction.send("Request timed out.", ephemeral=True)
              return
        else:
            await interaction.followup.send("Cannot erase stats that don't exist!", ephemeral=True)

# The pick command allows the user to pick the class they will use until they reset their stats, which takes the arguments Knight with a value of one, Archer with a value of 2, and Mage with a value of 3. It ensures first that the start value is 1, or in other words that the user has used start, if so the program continues, and it also checks if the pick command has already been used by checking if the value of the class column is either 1, 2, or 3 for each class respectively. Afterwards, whatever the value of the argument is, function will insert that value into the users table for that user. Additionally, it will send a message notifying the user that they selected their class with the class they chose, dependent on the value of the argument.
@client.slash_command(name = "pick", description = "Pick a class of your choice: Knight, Archer, or Mage!")
async def pck(interaction: Interaction, number: int = SlashOption(name="class", choices={"Knight": 1, "Archer": 2, "Mage": 3})):  
    await interaction.response.defer()
    async with db_pool.acquire() as cursor:

      start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)

      check_battle_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)

      check_battle_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)

      if start_value != 1:
        await interaction.followup.send("Cannot pick class when /start has not been used!")
      elif check_battle_one == 1 or check_battle_two == 1 or check_battle_one == 0 or check_battle_two == 0:
        await interaction.followup.send("Cannot pick a class during a battle! Wait until the battle ends or forfeit the battle when possible!")
      else:
        class_value = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', interaction.user.id)
        if class_value == 1 or class_value == 2 or class_value == 3:
           await interaction.followup.send("You have already picked a class! To pick a new class, you must reset your stats.")
        else:
          await cursor.execute('UPDATE users SET class = $1 WHERE user_id = $2', number, interaction.user.id)
          if number == 1:
            await interaction.followup.send("You picked the Knight class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 2:
            await interaction.followup.send("You picked the Archer class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 
          elif number == 3:
            await interaction.followup.send("You picked the Mage class! This is the class you will use during battles. To pick a new class, you must reset your stats.") 


@client.slash_command(name = "battle", description = "Battle an opponent of your choice in this server!")   
# gotten from: https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-
async def battle(interaction: Interaction, member: nextcord.Member):    #.battle command, request battles to other users
  global db_pool
  await interaction.response.defer()
  async with db_pool.acquire() as cursor:

    # Various 'select' queries to check various conditions.
    start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)
    class_value_initial = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', interaction.user.id)
    class_value_final = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', member.id)
    check_battle_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    check_battle_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    check_battle_three = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', member.id)
    check_battle_four = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', member.id)
    battle_requested = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    requesting_battle = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    requested_battle =  await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', member.id) # To check if the reciever has alraeady been requested for a battle.

  if start_value != 1: # Has the user used start?
    await interaction.followup.send("Please use /start and try again.")
    return
  elif class_value_initial != 1 and class_value_initial != 2 and class_value_initial != 3: # Has the starter picked a class?
    await interaction.followup.send("Please use /pick and try again.")
    return
  elif battle_requested == 0 or requesting_battle == 0: # Has the starter requested or been requested for a battle?
    await interaction.followup.send("You have already requested or been requested for a battle! Please await for your request to timeout or be accepted/rejected or accept/reject your request to try again.")
  elif check_battle_one == 1 or check_battle_two == 1: # Is the user in a battle?
    await interaction.followup.send("Cannot initiate another battle during a battle! Wait until the battle ends or forfeit the battle!")
  elif check_battle_three == 1 or check_battle_four == 1 or requested_battle == 0: # Is the reciever in a battle or has been requested for one already?
    await interaction.followup.send("Cannot battle someone who is already in a battle or has requested for a battle!")
  elif member.id == interaction.user.id: # Is the starter attempting to battle himself?
    await interaction.followup.send("You cannot battle yourself!")
  elif class_value_final != 1 and class_value_final != 2 and class_value_final != 3: # Has the reciever picked a class?
    await interaction.followup.send("Cannot battle user who has not picked a class!")
  else: # If the conditions have been met and none of the players are in a battle or have requested for one are requesting one, then battle can start being initialized.
    async with db_pool.acquire() as cursor:

      await cursor.execute('INSERT INTO battles (battle, starter_id, reciever_id) VALUES ($1, $2, $3)', 0, interaction.user.id, member.id) # Insert these temporary values, in which 0 as the battle value means both the starter (interaction.user.id), and the reciever (member.id) are in a battle request state. Also, interaction.channel_id ensures that a command such as /ff can only be used in the channel where the battle between these users was started.

    await interaction.followup.send(f"Before you fight {member.mention}, they must consent to your worthy request! \n {member.mention}, would you like to fight, {interaction.user.mention}? Respond `yes` or something similar to confirm, respond anything else to cancel.") # Send a message to inform both users of the battle and ask the reciever for their consent to the battle.  
    if battle_requested != 0: # If the starter has not started a battle request or has been requested for a battle then do what is below.
      # Below from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
      try:
        msg = await client.wait_for("message", timeout=60, check=lambda message: message.author.id == member.id and message.channel.id == interaction.channel_id) # Await for a message from the reciever.
      except asyncio.TimeoutError: # If 60 seconds have passed and the reciever hasn't responded, inform that the reciever took too long to respond and cancel the battle.
        await interaction.followup.send("User took too long to respond. Use /battle to try again.")
      # Above from https://www.youtube.com/watch?v=zamNFx3L7oA&t=2s&ab_channel=Dannycademy
        async with db_pool.acquire() as cursor:

          await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id)

        return 

      if msg.content.lower() in  ["yes", "ye", "yeah", "sure", "ok", "y", "k", "okay", "yeh", "ya", "kk",  "why not", "yess", "yah"]: # However, if the reciever strictly says "yes", do what is below.
          start_rand = random.choice([1,2]) #currently, we are deciding the person who gets first move by random
          await interaction.followup.send("Starting battle...") # Inform the users that the battle is starting.
          await battle_command.battle(interaction, member, start_rand, db_pool) # Call the battle function in the battle_command file and proceed.
      else: # If the reciever responds with anything else, cancel the battle.
          async with db_pool.acquire() as cursor:

            await interaction.followup.send("Battle request cancelled.")
            await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id) # Delete that battle instance row in the table as a result of the cancellation of the battle.

    else:
      return

# The stats command diplays the stats of a user that is mentioned, for now displaying the user's class only. The function checks that the start value is one for the user so stats can be actually displayed for the user. Then the value of the class column for that user is checked to display their class, which is then proceeded to deferring the need to respond to the interaction and then following up by sending the embed for the user's stats, which is for now only their class. If the user has not used the pick function ypet, the class displayed will simply be N/A.
@client.slash_command(name = "stats", description = "Display the stats for any person on the server!")
async def st(interaction: Interaction, member: nextcord.Member):    #.stats command, displays the stats of user's chosen class in an embed
  # member: nextcord.Member arg gotten from https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-argument
      async with db_pool.acquire() as cursor:

        class_value = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', member.id)
        global_level = await cursor.fetchrow('SELECT exp, level, exp_needed FROM global_levels WHERE user_id = $1 ', member.id)
        server_level = await cursor.fetchrow('SELECT exp, level, exp_needed FROM server_levels WHERE user_id = $1 AND guild_id = $2', member.id, interaction.guild_id)
        rank_data = await cursor.fetch(f"""
            SELECT user_id
            FROM server_levels
            WHERE guild_id = $1
            ORDER BY level DESC, exp DESC
        """, interaction.guild_id)

      if class_value == 1:
         class_value = "Knight"
      elif class_value == 2:
        class_value = "Archer"
      elif class_value == 3:
        class_value = "Mage"
      else:
        class_value = "No class data to show."

      if global_level is not None:
        global_level_value = global_level[1]
        global_exp_ratio = f"{global_level[0]}/{global_level[2]}"
        global_next_level = global_level_value + 1
      else:
        global_level_value = "N/A"
        global_exp_ratio = "N/A"
        global_next_level = "N/A"

      if server_level is not None:
        server_level_value = server_level[1]
        server_exp_ratio = f"{server_level[0]}/{server_level[2]}"
        server_next_level = server_level_value + 1
        rank = 1
        for record in rank_data:
          if record['user_id'] == member.id:
            break
          else:
            rank += 1
      else:
        rank = "N/A"
        server_level_value = "N/A"
        server_exp_ratio = "N/A"
        server_next_level = "N/A"

      embed_st = Embed(   
        title = f"Stats for {member}:",     
        color = nextcord.Color.blue())
      embed_st.add_field(
        name = "Class:",
        value = f"\n {class_value} \n",)    
      embed_st.add_field(    
        name="Levelling Across Servers: ", 
        value= f"Level: **{global_level_value}** \n \n XP Needed for Level **{global_next_level}**: \n \n **__{global_exp_ratio}__**",
        inline = False,)
      embed_st.add_field(    
        name=f"Levelling for **__{interaction.guild}__**: ", 
        value= f"Level: **{server_level_value}** \n \n XP Needed for Level **{server_next_level}**: \n \n **__{server_exp_ratio}__** \n \n **__Server Rank__**: **{rank}**",
        inline = False,)
      await interaction.response.defer()
      await interaction.followup.send(embed=embed_st)

@client.event
async def on_disconnect():
    try:
      logging.info("Commencing cleanup procedure...")
      async with db_pool.acquire() as cursor:
        logging.info("Ending ALL battles...")
        await cursor.execute("DELETE FROM battles")
        await cursor.execute("DELETE FROM cooldowns")
        await cursor.execute("DELETE FROM moves")
      await close_pool()
      client.unload_extension("cogs.levels")
    except Exception as e:
      logging.error(f"Error in on_disconnect: {e}")

# Below from https://docs.replit.com/tutorials/python/build-basic discord-bot-python

if not asyncio.get_event_loop().is_running():
  my_secret = os.environ['DISCORD_BOT_SECRET']
  handle_shutdowns()
  client.run(my_secret)  