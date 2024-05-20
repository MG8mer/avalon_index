import os
import nextcord
from nextcord.ext import commands
import math
import random
import logging
import asyncpg

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # define client

class Leveling(commands.Cog):#level system function
  def __init__(self, client):
    self.client = client
    self.db_pool = client.db_pool

  async def ensure_pool(self):
    if self.db_pool is None or self.db_pool._closed:
      logging.warning("Database pool needs to be reinitialized.")
      await self.client.create_db_pool()
      self.db_pool = self.client.db_pool
    
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot or message.content == ".shutdown":
      return
    else:
      await self.ensure_pool()
      async with self.db_pool.acquire() as cursor:
        await cursor.execute("""CREATE TABLE IF NOT EXISTS levels(user_id BIGINT, guild_id BIGINT, exp INTEGER, level INTEGER, last_lvl INTEGER)""") # Create levels table if it doesn't exist.
      try: #will try to grab the exp, levels, and etc. from database
        async with self.db_pool.acquire() as cursor:
          result = await cursor.fetchrow(f"SELECT user_id, guild_id, exp, level, last_lvl FROM levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
      except AttributeError:
        return
      async with self.db_pool.acquire() as cursor:
        start_value = await cursor.fetchval(f'SELECT start FROM users WHERE user_id = {message.author.id}')
      if result is None:  #if there is no data in result, it will add the base levels and exp to that particular user
        async with self.db_pool.acquire() as cursor:
          await cursor.execute(f"INSERT INTO levels (user_id, guild_id, exp, level, last_lvl) VALUES ({message.author.id},{message.guild.id}, 0, 0, 0)")
      elif start_value == 1: #if the user has already started the bot, it will store the existing levels, exp, and etc. in their respective variables below
        exp = result[2]
        lvl = result[3]
        last_lvl = result[4]
        exp_gained = random.randint(1, 5)
        exp += exp_gained #adds the exp gained to the exp variable
        lvl = 0.1 * math.sqrt(exp)
        async with self.db_pool.acquire() as cursor:
          await cursor.execute(f"UPDATE levels SET exp = {exp}, level = {lvl}, last_lvl = {last_lvl} WHERE user_id = {message.author.id}") #updates the user's exp, level, and last level
        if int(lvl // 1) == last_lvl + 1: 
          last_lvl = int(lvl // 1)
          async with self.self.db_pool.acquire() as cursor:
            await cursor.execute(f"UPDATE levels SET last_lvl = {last_lvl} WHERE user_id = {message.author.id}") #updates database to their new level
          embed = nextcord.Embed(title=f"**__Congratulations!__**",
            description=f"You have reached level {last_lvl}!",
            colour=0x00b0f4)
          embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
          embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
          await message.author.send(embed=embed) #sends the embed in dms to notify the user that they have reached a new leve
      else:
        return

def setup(client):
  client.add_cog(Leveling(client)) # Add cog for leveling

# Leveling system above from https://youtu.be/55KLwf8P1ec?si=vROVGsVjML_iUazm