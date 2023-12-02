import nextcord
from nextcord.embeds import Embed
import randGIF
from datetime import datetime
import nextcord.interactions

# Below is the second page from the help function, which lists the first few important commands in the Avalon Index in case the user is confused.

async def help(interaction, bot_name, bot_avatar_url):
  botName = bot_name
  bot_avatar_url = bot_avatar_url
  url = randGIF.randgif("HELP ME")
  embed = Embed(title="Avalon Index's Help Menu", #main embed field, with title and description
    description=f"All necessary commands to play the game to your heart's content! {interaction.user.mention}",
    colour=nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(name=botName, #author field
    icon_url=bot_avatar_url)
  embed.add_field(name="> .gif", #.gif embed
    value="Use this command to generate a gif of your theme!",
    inline=True)
  embed.add_field(name="> Syntax", #.gif embed, additional field for correct usage
    value="```\n.gif <search_term>\n```",
    inline=True)
  embed.set_image(url=f"{bot_avatar_url}")
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  # We then proceed to defer the need to respond to the interaction and then followup by sending the embed for the second help page.
  await interaction.response.defer()
  await interaction.followup.send(embed=embed)    #.help command, lists all possible commands in this game
