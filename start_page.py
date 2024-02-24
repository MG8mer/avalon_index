import nextcord
import nextcord.embeds
import nextcord.interactions
from nextcord import Interaction
import aiosqlite
import randGIF

# Below is a function to check specific values of the user that used the start function in addition to counting the amount of players registered with the bot.
async def check_assign(interaction: Interaction):
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT * FROM users')
      user_data = await cursor.fetchall() # Fetch all the data in the users table for player count.
      await cursor.execute('SELECT start FROM users WHERE user_id = ?', (interaction.user.id,))
      start_value = await cursor.fetchone() # For if they already used start.
      await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
      check_battle_one = await cursor.fetchone() # Check if the user is in a battle where they are the starter.
      await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
      check_battle_two = await cursor.fetchone() # Check if the user is in a battle where they are the reciever.
      user_count = 0 
      archive_i = 0 # For the for conditional
      user_data_concatenated = ()
      if user_data != None: # If the user_data has actual data to iterate through
        for j in range(len(user_data)): 
          user_data_concatenated += user_data[j] # For the length of user_data, add each value of user_data into a new tuple to properly store the data of all the users.
        for i in range(len(user_data_concatenated)):
          if i == 3 or i - archive_i == 4: 
            user_count += 1 # For the length of the new tuple, if the value of i is 3 or if the difference between archive_i and i is 4, add 1 to the user_count to indicate that the loop has detected one user in the data base.
            archive_i = i # Store that i value when the for loop condition was fulfiled to be checked later.
      return start_value, check_battle_one, check_battle_two, user_count # Return the value of start, check_battle_one (will be 1 if the user is a starter in a battle), check_battle_two (will be 1 if the user is a reciever in a battle), and the amount of users.
    await db.commit()


#this is the start page, the first page the players will see when they get started w the bot, sending an embed with useful information.
async def start(interaction, bot_name, bot_avatar_url):
  botName=bot_name
  emoji = 'https://tenor.com/view/tower-defense-simulator-roblox-itzsweaking-mario-minecraft-gif-21237948'
  url = randGIF.randgif("GOOD LUCK RPG VIDEO GAME")
  
  start_value, check_battle_one, check_battle_two, user_count = await check_assign(interaction)
  
  embed = nextcord.Embed(title=f"**__Welcome to Avalon Index!__**",
    description=f"Hey {interaction.user.mention}! **__Avalon Index__** is a simple turn-based RPG game developed by **Hamzeus, Po, and Avash**. Currently, there are **__{user_count} users registered, including yourself!__** To get started, follow the steps below. We hope you enjoy!", 
    colour=0x00b0f4)
  embed.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(name="**Pick Your Class**",
    value="You must pick **1** out of the **3** currently available classes to accompany you on your journey. Use ``/pick`` command once ready.",
    inline=False)
  embed.add_field(name="**Knight** `1`",
    value="The Knight is the tankiest class in the game and is a **__close ranger__**.",
    inline=True)
  embed.add_field(name="**Archer** `2`",
    value="The Archer has amazing and deadly **__long range__** capabilities but is the weakest.",
    inline=True)
  embed.add_field(name="**Mage** `3`",
    value="The Mage is a **__mid ranger__** class and lacks in both defense and damage.",
    inline=True)
  embed.add_field(name="**Having Trouble Picking A Class?**",
    value="We've provided you with the base stats of each class to help you pick the best fit class! Use ``/about`` command to display the base stats of a class.",
    inline=False)
  embed.add_field(name="**Need Help?**",
    value="If you need further guidance with proper command usage, use ``/help`` command to gain more knowledge before heading off.",
    inline=False)
  # embed.set_image(url=bot_avatar_url)
  embed.set_image(url=url)
  embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the start page.
  await interaction.response.defer()
  await interaction.followup.send(embed=embed)