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



# Database connect along with cursor method and database commit method all throughout main.py from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik

import os
import requests
from pprint import pprint
from nextcord import Interaction # from https://www.youtube.com/watch?v=zvVziW2qS-0&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=17&t=558s&ab_channel=JamesS
import nextcord # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
import asyncio # from https://docs.python.org/3/library/asyncio.html
import aiosqlite # from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
from nextcord.application_command import SlashOption # from https://www.youtube.com/watch?v=gtSbqUJLpvM&t=238s&ab_channel=Civo
from nextcord.embeds import Embed # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext import commands # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from nextcord.ext.commands import context    #from https://docs.replit.com/tutorialsb/python/build-basic-discord-bot- python and # from https://www.youtube.com/watch?v=wn7NIqSSgas&list=PL-7Dfw57ZZVRB4N7VWPjmT0Q-2FIMNBMP&index=16&ab_channel=JamesS
from active import active  
import about_archer
import about_knight
import about_mage
import help_page
import help_pageTWO
import start_page


active() # from https://docs.replit.com/tutorials/python/build-basic-discord-bot-python

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all())   #from https://youtu.be/ksAtGCFxrP8#si=A89Nokdcqfsy_tGZ
client.remove_command('help') # Removing the built in help command 


@client.command()
async def gif(ctx, *args): #prefix command to grab gif based on arg
 if len(args) != 1:
   await ctx.send("Usage: ``.gif <search_term>``. Check ``.help`` for more info") #usage error
 else:
  arg = args[0]
  print (f"{arg}")
  search_term = arg
  lim = 1
  media_filter = "gif, tinygif"
  random = True
  SECRET_KEY = os.environ["TENOR_API_KEY"]
  ckey = "my_client_key"

  try:
    r = requests.get(
      f"https://tenor.googleapis.com/v2/search?q={search_term}&key={SECRET_KEY}&client_key={ckey}&limit={lim}&media_filter={media_filter}&random={random}") #requests api for an obj containing our results
    r.raise_for_status()
  except requests.exceptions.RequestException as e:
    print(f"Error making API request: {e}")
    await ctx.send("Error fetching GIF. Please try again later.")
    return

  if r.status_code == 200:
    data = r.json()
    pprint(data)
    print(r.status_code)
    url = data['results'][0]['media_formats']['gif']['url'] #opens the json obj and grabs the gif url
    print(url)
    embed = Embed(title="The GIF Machine", 
                  description=f"Here's your GIF! {ctx.author.mention}", 
                  color=0x00ff00)
    embed.set_image(url=f"{url}")
    embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/qY14QUB9KPYAAAAi/tenor-stickers.gif")
    await ctx.send(embed=embed) #sends the gif and deletes the user msg to not clutter the chat
    await ctx.message.delete()
  else:
    print("No results found.")
    embed = Embed(title="No Results Found")
    await ctx.send(embed=embed)
    await ctx.message.delete() #a prefix command to get a gif based on the arguement

@client.event
async def on_ready(): # from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  print("Bot is up") #prints when bot is online from https://docs.replit.com/tutorials/python/build-basic-discord-bot- python
  # Table creation from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('CREATE TABLE IF NOT EXISTS users(user_id INTEGER, guild_id INTEGER, class INTEGER, start INTEGER)')
    await db.commit()
  print(f"{len(client.guilds)}")
  print(f"{client.guilds[0].id}")

@client.slash_command(name = "help", description = "Are you confused?") #slash command to print out help pages
async def help(interaction: Interaction, number: int = SlashOption(name="page", choices={"#1": 1, "#2": 2})):
    botName = client.user.name
    bot_avatar_url = client.user.avatar.url
    if number == 1: 
        await help_page.help(interaction, botName, bot_avatar_url)
    elif number == 2: 
        await help_pageTWO.help(interaction, botName, bot_avatar_url)

# The start command essentially starts the game for the user that uses the command and allows them to use commands such as stats, battle, pick, and so on. It does this by creating a new section in the users table and setting the start value column to one. Additionally, the other functions rely on this value by checking if the start value is one, or in other words if the user used the start command, if the user did not use the command, the user won't be able to use the other functions. Additionally, if the user already used start, the command will not work by checking the start value. The command also sends an embed explaining the game and hot to get started.
# Start command implementation code from https://www.youtube.com/watch?v=aBm8OVxpJno&ab_channel=Glowstik
@client.slash_command(name = "start", description = "Starts the game!")
async def start(interaction: Interaction):    #/start command, to start the game users must type this first
  botName = client.user.name
  bot_avatar_url = client.user.avatar.url
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone()
      if start_value == (1,):
         await interaction.response.send_message("You have already used start! If you would like to reset your stats, please use the /reset command.")
      else:
        await cursor.execute('INSERT INTO users (user_id, guild_id, start) VALUES (?, ?, ?)', (interaction.user.id,client.guilds[0].id, 1))
        await start_page.start(interaction, botName, bot_avatar_url)
    await db.commit()

# Button implementation for reset command and reset command implementation from https://www.youtube.com/watch?v=y3TqSUSOprs&ab_channel=Glowstik

# The class below creates the interaction buttons that are present in the message sent by the bot when /reset is used.
class ConfirmDeny(nextcord.ui.View):
  def __init__(self):
    super().__init__()
    self.value = None

# The function below creates the "yes" button for the reset function, which is red is color, and what it does is it deletes the row in the table of the user that used /reset, resetting their stats and allowing them to use /reset again. Additinally, after the button is pressed, it cannot be pressed again, as the buttons stop working.
  @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green)
  async def y(self, button: nextcord.ui.Button, interaction: Interaction):
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute('DELETE FROM users WHERE user_id = ?', (interaction.user.id,))
        await interaction.response.send_message('Stats successfully deleted. You may use /start to get started again!', ephemeral=True) # Ephermeral makes the message only visible to the user that used the command.
      await db.commit()
    self.value = True
    self.stop()
    
# The function below creates the "no" button for the reset function, which is red in color. It merely cancels the command by responding to the interaction by sending a message that says the request was cancelled.
  @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red)
  async def n(self, button: nextcord.ui.Button, interaction: Interaction):
    await interaction.response.send_message('Request cancelled.', ephemeral=True)
    self.value = False
    self.stop()

# The reset function below implements the ConfirmDeny class created above and ensures to wait for the user to press a button and eventually times out. Additionally, the function checks that start value is one in the users table so that stats can actually be deleted.
@client.slash_command(name = "reset", description = "Reset your stats and pick a new class.")
async def re(interaction: Interaction):
  view = ConfirmDeny()
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone()
      if start_value == (1,):
         await interaction.response.send_message("Hold up! Once you reset your stats, you cannot go back, are you sure you want to proceed?", view=view, ephemeral=True)
         await view.wait()
      else:
         await interaction.response.send_message("Cannot erase stats that don't exist!", ephemeral=True)
      await db.commit()
  if view.value is None:
    return

# The pick command allows the user to pick the class they will use until they reset their stats, which takes the arguments Knight with a value of one, Archer with a value of 2, and Mage with a value of 3. It ensures first that the start value is 1, or in other words that the user has used start, if so the program continues, and it also checks if the pick command has already been used by checking if the value of the class column is either 1, 2, or 3 for each class respectively. Afterwards, whatever the value of the argument is, function will insert that value into the users table for that user. Additionally, it will send a message notifying the user that they selected their class with the class they chose, dependent on the value of the argument.
@client.slash_command(name = "pick", description = "Pick a class of your choice: Knight, Archer, or Mage!")
async def pck(interaction: Interaction, number: int = SlashOption(name="class", choices={"Knight": 1, "Archer": 2, "Mage": 3})):    #.pick command, to pick a class users must type this command
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone()
      if start_value != (1,):
        await interaction.response.send_message("Cannot pick class when /start has not been initialized!")
      else:
        await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
        class_value = await cursor.fetchone()
        if class_value == (1,) or class_value == (2,) or class_value == (3,):
           await interaction.response.send_message("You have already picked a class! To pick a new class, you must reset your stats or die three times in three consecutive battles.")
        else:
          await cursor.execute('UPDATE users SET class = ? WHERE user_id = ?', (number, interaction.user.id))
          if number == 1:
            await interaction.response.send_message("You picked the Knight class! This is the class you will use during battles. To pick a new class, you must reset your stats or die three times in three consecutive battles.") 
          elif number == 2:
            await interaction.response.send_message("You picked the Archer class! This is the class you will use during battles. To pick a new class, you must reset your stats or die three times in three consecutive battles.") 
          elif number == 3:
            await interaction.response.send_message("You picked the Mage class! This is the class you will use during battles. To pick a new class, you must reset your stats or die three times in three consecutive battles.") 
    await db.commit()

# The stats command diplays the stats of a user that is mentioned, for now displaying the user's class only. The function checks that the start value is one for the user so stats can be actually displayed for the user. Then the value of the class column for that user is checked to display their class, which is then proceeded to deferring the need to respond to the interaction and then following up by sending the embed for the user's stats, which is for now only their class. If the user has not used the pick function yet, the class displayed will simply be N/A.
@client.slash_command(name = "stats", description = "Displays stats of your character")
async def st(interaction: Interaction, member: nextcord.Member):    #.stats command, displays the stats of user's chosen class
  # member: nextcord.Member arg gotten from https://stackoverflow.com/questions/68646719/discord-py-set-user-id-as-an-argument
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (member.id,))
      start_value = await cursor.fetchone()
      if start_value != (1,):
        await interaction.response.send_message("Cannot view stats that don't exist!")
      else:
        await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
        class_value = await cursor.fetchone()
        if class_value == (1,):
          embed_stk = Embed(   
            title = "Stats:", 
            color = nextcord.Color.blue())
          embed_stk.add_field(    
              name="Class:", 
              value="Knight",)
          await interaction.response.defer()
          await interaction.followup.send(embed=embed_stk)
        elif class_value == (2,):
          embed_sta = Embed(   
            title = "Stats:", 
            color = nextcord.Color.blue())
          embed_sta.add_field(    
              name="Class:", 
              value="Archer",)
          await interaction.response.defer()
          await interaction.followup.send(embed=embed_sta)
        elif class_value == (3,):
          embed_stm = Embed(   
            title = "Stats:", 
            color = nextcord.Color.blue())
          embed_stm.add_field(    
            name="Class:", 
            value="Mage",)
          await interaction.response.defer()
          await interaction.followup.send(embed=embed_stm)
        else:
          embed_stn = Embed(   
            title = "Stats:", 
            color = nextcord.Color.blue())
          embed_stn.add_field(    
            name="Class:", 
            value="N/A",)
          await interaction.response.defer()
          await interaction.followup.send(embed=embed_stn)
    await db.commit()


@client.slash_command(name = "about", description = "Learn more about each class!") #slash command to print out info on the three classes, based on user arg, it will call a function from another py file and send an embed on the corresponding class
async def about(interaction: Interaction, number: int = SlashOption(name = "class", choices = {"Knight": 1, "Archer": 2, "Mage": 3})):
    if number == 1: 
        await (about_knight.about(interaction))
    elif number == 2: 
        await (about_archer.about(interaction))
    elif number == 3: 
        await (about_mage.about(interaction))

@client.event    #from https://youtu.be/ksAtGCFxrP8?si=A89Nokdcqfsy_tGZ
async def on_member_join(member):  #server notification on member join
    channel = client.get_channel(1173135610605740082) 
    if isinstance(channel, nextcord.TextChannel): 
        await channel.send(f'Hi @{member.name}, use .help to use the Avalon Index!') 

@client.event    #from https://youtu.be/ksAtGCFxrP8?si=A89Nokdcqfsy_tGZ
async def on_member_remove(member):    #server notification on member leave
  channel = client.get_channel(1173135610605740082)
  if isinstance(channel, nextcord.TextChannel): 
    await channel.send(f'We are sorry to see you go @{member.name} :sob:')

# Below from https://docs.replit.com/tutorials/python/build-basic discord-bot-python
my_secret = os.environ['DISCORD_BOT_SECRET']    
client.run(my_secret)  