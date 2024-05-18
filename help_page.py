# We import the nextcord library, embeds from nextcord.embeds for aesthetic, interactions for slash comamnd support on discord, and the randGIF file in our repo to generate a random gif in the embed.

import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
import randGIF

      
# Below is the first page from the help function, which lists the first few important commands in the Avalon Index in case the user is confused.

async def help(interaction, bot_name, bot_avatar_url):
  botName = bot_name
  bot_avatar_url = bot_avatar_url
  url = randGIF.randgif("HELP ME")
  embed = Embed(    #main embed field, with title and description
    title = f"**{botName}'s Help Menu (pg. 1)**", 
    description = f"All the necessary commands to play the game to your heart's content! {interaction.user.mention}", 
    color = nextcord.Color.blue())
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
    name="> /about", 
    value="Learn more about each class!",
    inline=True)
  embed.add_field(    #.about embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/about <class: Knight *or* Archer *or* Mage>```\n", 
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
    value="Displays stats of your character", 
    inline=True)
  embed.add_field(    #.stats embed, additional field for correct usage
    name="> Syntax", 
    value="```\n/stats <member: **must be present within the same server!**>\n```", 
    inline=True)
  embed.add_field(    #.moves embed
    name="> /reset", 
    value="Reset your stats and start from scratch!", 
    inline=False)
  embed.add_field(    #.ff embed
    name="> FF",     
    value="Forfeiting a battle can now be done by simply pressing the red `FF` button on your battle embed!", 
    inline=False)
  embed.set_thumbnail(url=f"{url}")
  embed.set_image(url=f"{bot_avatar_url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the first help page.
  await interaction.response.defer()
  await interaction.followup.send(embed=embed)    #.help command, lists all possible commands in this game