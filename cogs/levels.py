import os
import nextcord
from nextcord.ext import commands
import math
import random
import asyncpg
import time
import logging
from main import ensure_db_pool
from nextcord.utils import get
from collections import defaultdict
from shared import role_designation

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # define client

last_message_time = defaultdict(lambda: 0)

message_between_time = 60

class Leveling(commands.Cog):#level system function
  def __init__(self, client):
    self.client = client
    self.db_pool = client.db_pool

  @commands.Cog.listener()
  async def on_message(self, message):
    current_time = time.time()
    if message.author.bot or message.content == ".shutdown":
      return
    else:
        await ensure_db_pool(self.db_pool)
        async with self.db_pool.acquire() as cursor:
          no_roles = await cursor.fetch("SELECT role_id FROM no_exp_roles WHERE guild_id = $1", message.guild.id)
        if no_roles != []:
            formatted_roles = []
            user_roles = [role.id for role in message.author.roles if role.name != "@everyone"]
            for id_role in no_roles:
              formatted_roles.append(id_role['role_id'])

            for roles in user_roles:
              if roles in formatted_roles:
                return

        async with self.db_pool.acquire() as cursor:
          no_channels = await cursor.fetch("SELECT channel_id FROM no_exp_channels WHERE guild_id = $1", message.guild.id)
        if no_channels != []:
            formatted_channels = []
            for id_channel in no_channels:
              formatted_channels.append(id_channel['channel_id'])

            for channels in formatted_channels:
              if message.channel.id in formatted_channels:
                return
        try:
          async with self.db_pool.acquire() as cursor:
            server_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM server_levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
        except AttributeError:
          return

        if server_result is None: 
          async with self.db_pool.acquire() as cursor:
            exp_needed = round(100*(pow(1, 1.1)))
            await cursor.execute(f"INSERT INTO server_levels (user_id, guild_id, exp, level, exp_needed) VALUES ({message.author.id}, {message.guild.id}, 0, 0, {exp_needed})")

        if current_time - last_message_time[message.author.id] >= message_between_time:
          last_message_time[message.author.id] = current_time
          exp_gained = random.randint(25, 50)
          if server_result is not None:
              server_exp = server_result[0]
              server_lvl = server_result[1]
              server_exp_needed = server_result[2]
              msg_words = message.content.split()
              if len(msg_words) > 10:
                exp_gained = round(exp_gained * 1.2)

              async with self.db_pool.acquire() as cursor:
                boosted_roles = await cursor.fetch("SELECT role_id FROM exp_boosted_roles WHERE guild_id = $1", message.guild.id)
              if boosted_roles != []:
                  formatted_roles = []
                  user_roles = [role.id for role in message.author.roles if role.name != "@everyone"]
                  for id_role in boosted_roles:
                    formatted_roles.append(id_role['role_id'])

                  boosted_exp_roles = []

                  for roles in user_roles:
                    if roles in formatted_roles:
                      boosted_exp_roles.append(roles)

                  if boosted_exp_roles != []:
                    boost_percents = []
                    async with self.db_pool.acquire() as cursor:
                        for role_id in boosted_exp_roles:
                            boost_val = await cursor.fetchval(
                                f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {role_id} AND guild_id = {message.guild.id}")
                            boost_percents.append((role_id, boost_val))

                    boosted_exp_roles = [role_id for role_id, _ in boost_percents]
                    async with self.db_pool.acquire() as cursor:
                       boost_val = await cursor.fetchval(f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {boosted_exp_roles[0]} AND guild_id = {message.guild.id}")

                    boosted_role = nextcord.utils.get(message.guild.roles, id=boosted_exp_roles[0])
                    exp_gained = round(exp_gained * ((boost_val/100)+1))

              server_exp += exp_gained 
              async with self.db_pool.acquire() as cursor:
                await cursor.execute(f"UPDATE server_levels SET exp = {server_exp} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}") 

              while server_exp >= server_exp_needed: 
                  server_lvl += 1
                  exp_surplus = server_exp - server_exp_needed
                  server_exp_needed = round(100*(pow((server_lvl+1), 1.1)))
                  async with self.db_pool.acquire() as cursor:
                    await cursor.execute(f"UPDATE server_levels SET exp = {exp_surplus}, level = {server_lvl}, exp_needed = {server_exp_needed} WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}") 
                  embed = nextcord.Embed(title=f"**__Congratulations!__**",
                    description=f"You have reached level {server_lvl}!",
                    colour=0x00b0f4)
                  embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
                  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
                  async with self.db_pool.acquire() as cursor:
                    levelup_channel = await cursor.fetchval("SELECT channel_id FROM level_up_channel WHERE guild_id = $1", message.guild.id)

                  if levelup_channel is None:
                    await message.channel.send(f"{message.author.mention}", embed=embed)
                  else:
                    channel_set = get(message.guild.channels, id=levelup_channel)
                    await channel_set.send(f"{message.author.mention}", embed=embed)
                  await role_designation(message.author, message.author.id, message.guild, message.guild.id, message.channel, server_lvl, self.db_pool)

def setup(client):
  client.add_cog(Leveling(client)) # Add cog for leveling

# Leveling system above inspired from https://youtu.be/55KLwf8P1ec?si=vROVGsVjML_iUazm