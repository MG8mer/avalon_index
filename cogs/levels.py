import nextcord
from nextcord.ext import commands
import vacefron 
import math
import random
import sqlite3

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())

database = sqlite3.connect("main.db")
cursor = database.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS levels (user_id INTEGER, guild_id INTEGER, exp INTEGER, level INTEGER, last_lvl INTEGER)""")

class Leveling(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.author.bot:
      return
    else:
      try:
        cursor.execute(f"SELECT user_id, guild_id, exp, level, last_lvl FROM levels WHERE user_id = {message.author.id} AND guild_id = {message.guild.id}")
      except AttributeError:
        return
      result = cursor.fetchone()
      cursor.execute(f'SELECT start FROM users WHERE user_id = {message.author.id}')
      start_value = cursor.fetchone()
      if result is None:
        cursor.execute(f"INSERT INTO levels (user_id, guild_id, exp, level, last_lvl) VALUES ({message.author.id}, {message.guild.id}, 0, 0, 0)")
        database.commit()
      elif start_value == (1,):
        exp = result[2]
        lvl = result[3]
        last_lvl = result[4]
        exp_gained = random.randint(1, 5)
        exp += exp_gained
        lvl = 0.1 * math.sqrt(exp)
        cursor.execute(f"UPDATE levels SET exp = {exp}, level = {lvl}, last_lvl = {last_lvl} WHERE user_id")
        if int(lvl // 1) == last_lvl + 1:
          last_lvl = int(lvl // 1)
          cursor.execute(f"UPDATE levels SET last_lvl = {last_lvl} WHERE user_id")
          embed = nextcord.Embed(title=f"**__Congratulations!__**",
            description=f"You have reached level {last_lvl}!",
            colour=0x00b0f4)
          embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
          embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
          await message.author.send(embed=embed)
        database.commit()
      else:
        return

def setup(client):
  client.add_cog(Leveling(client))


