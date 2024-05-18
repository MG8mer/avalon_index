import os
import nextcord
import nextcord.embeds
import nextcord.interactions
from nextcord import Interaction
from nextcord.ext import commands
import asyncpg
import randGIF

# Below is a function to check specific values of the user that used the start function in addition to counting the amount of players registered with the bot.
async def check_assign(interaction: Interaction, db_pool):
  async with db_pool.acquire() as cursor:
    user_data = await cursor.fetch('SELECT start FROM users')
    start_value = await cursor.fetchval('SELECT start FROM users WHERE user_id = $1', interaction.user.id)
    check_battle_one = await cursor.fetchval('SELECT battle FROM battles WHERE starter_id = $1', interaction.user.id)
    check_battle_two = await cursor.fetchval('SELECT battle FROM battles WHERE reciever_id = $1', interaction.user.id)
    user_count = 0 
    if user_data != None: 
      for data in user_data:
        user_count += 1

  return start_value, check_battle_one, check_battle_two, user_count # Return the value of start, check_battle_one (will be 1 if the user is a starter in a battle), check_battle_two (will be 1 if the user is a reciever in a battle), and the amount of users.


#this is the start page, the first page the players will see when they get started w the bot, sending an embed with useful information.
async def start(interaction: Interaction, bot_name, bot_avatar_url, db_pool):
  botName=bot_name
  emoji = 'https://tenor.com/view/tower-defense-simulator-roblox-itzsweaking-mario-minecraft-gif-21237948'
  url = randGIF.randgif("GOOD LUCK RPG VIDEO GAME")

  start_value, check_battle_one, check_battle_two, user_count = await check_assign(interaction, db_pool)

  embed = nextcord.Embed(title=f"**__Welcome to Avalon Index!__**",
    description=f"Hey {interaction.user.mention}! **__Avalon Index__** is a simple turn-based RPG game developed by **Hamzeus, Po, and Avash**. Currently, there are **__{user_count} users registered, including yourself!__** To get started, follow the steps below. We hope you enjoy!", 
    colour=0x00b0f4)
  embed.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(name="**Pick Your Class**",
    value="You must pick **1** out of the **3** currently available classes to accompany you on your journey. Use ``/pick`` command once ready.",
    inline=False)
  embed.add_field(name="**Knight** `1`",
    value="The Knight is the tankiest class in the game, with high HP, but low damagae.",
    inline=True)
  embed.add_field(name="**Archer** `2`",
    value="The Archer has high damage but lacks in terms of health.",
    inline=True)
  embed.add_field(name="**Mage** `3`",
    value="The Mage is a class with reliable damage and HP.",
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
  await interaction.followup.send(embed=embed)