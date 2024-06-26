# We import the nextcord library, embeds from nextcord.embeds for aesthetic, interactions for slash comamnd support on discord, and the randGIF file in our repo to generate a random gif in the embed.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from datetime import datetime
import randGIF


# Below is the first page from the help function, which lists the first few important commands in the Avalon Index in case the user is confused.

async def help(interaction, bot_name, bot_avatar_url):
  botName = bot_name
  bot_avatar_url = bot_avatar_url
  url = randGIF.randgif("HELP ME")
  embed = Embed(    #main embed field, with title and description
    title = f"**{botName}'s Help Menu (pg. 1)**", 
    description=f"All the commands for Avalon Index, including moderator and user ones! {interaction.user.mention}", 
    color = nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(    #author field
    name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(    #.start embed
    name="> /start", 
    value="Starts the game!", 
    inline=False)
  embed.add_field(    #.pick embed
    name="> /pick", 
    value="Pick a class of your choice: Knight, Archer, or Mage!",
    inline=True)
  embed.add_field(    #.pick embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/pick <class: Knight *or* Archer *or* Mage>\n```", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(    #.about embed
    name="> /avi_manual", 
    value="Learn more about the game Avalon Index and each class!",
    inline=True)
  embed.add_field(    #.about embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/about <page: General (general info on Avalon Index) *or* Knight *or* Archer *or* Mage>```\n", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(    #.battle embed
    name="> /battle", 
    value="Battle an opponent of your choice!", 
    inline=True)
  embed.add_field(    #.battle embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/battle <member: **must be present within the same server!**>\n```", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(    #.stats embed
    name="> /stats", 
    value="Displays somebody's stats (class/levelling).", 
    inline=True)
  embed.add_field(    #.stats embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/stats <member: **must be present within the same server!**>\n```", 
    inline=True)
  embed.add_field(    
    name="> /reset", 
    value="Reset your stats and start from scratch!", 
    inline=False)
  embed.add_field(name="> /gif", #.gif embed
    value="Use this command to generate a gif of your choice!",
    inline=True)
  embed.add_field(name="> Syntax", #.gif embed, additional field for correct usage
    value="```\n/gif <search_term>\n```",
    inline=True)
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  return embed