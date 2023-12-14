import nextcord
from nextcord.ext import commands
import vacefron 
import math
import random
import sqlite3

database = sqlite3.connect("database.sqlite")
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS levels (user_id INTEGER, exp INTEGER, level INTEGER, last_lvl INTEGER)""")

class Leveling(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
      cursor.execute(f"SELECT user_id, guild_id, exp, level, last_lvl FROM levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
      result = cursor.fetchone()
      if result is None:
        cursor.execute(f"INSERT INTO levels (user_id, guild_id, exp, level, last_lvl) VALUES ({message.author.id}, {message.guild.id}, 0, 0, 0)")
        database.commit()
      else:
        exp = result[2]
        lvl = result[3]
        last_lvl = result[4]
        exp_gained = random.randint(1, 5)
        exp += exp_gained
        lvl = 0.1 * math.sqrt(exp)
        cursor.execute(f"UPDATE levels SET exp = {exp}, level = {lvl}, last_lvl = {last_lvl} WHERE user_id")
        database.commit()

def setup(bot):
  bot.add_cog(Leveling(bot))