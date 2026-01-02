import nextcord
from nextcord.embeds import Embed
import randGIF
from datetime import datetime
import nextcord.interactions

# Below is the second page from the help function, which lists other important commands in Avalon Index in case the user is confused.

async def help(interaction, bot_name, bot_avatar_url):
  botName = bot_name
  bot_avatar_url = bot_avatar_url
  url = randGIF.randgif("HELP ME")
  embed = Embed(title = f"**{botName}'s Help Menu (pg. 2)**",
    description=f"All the commands for Avalon Index, including moderator and user ones! *For more info on global/server levels, see the General page of the `/avi_manual` command.* {interaction.user.mention}",
    colour=nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(name=botName, #author field
    icon_url=bot_avatar_url)
  embed.add_field(    
    name="> /playercount", 
    value="View the amount of users that have used `/start` and the amount of them that have used `/pick` to pick their class!", 
    inline=False)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="> /leaderboard", 
    value="View the rankings of people's server levels and server XP on this server! Compete to reach the top!", 
    inline=False)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="> /see_level_roles",
    value="See the roles awarded when reaching a particular server level on this server!", 
    inline=False)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(    
    name="> /see_exp_boosted_roles", 
    value="See the roles that gain extra server XP when messaging/battling on this server along with their % boost!", 
    inline=False)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="> /see_no_exp_roles",
    value="See the roles on this server that cannot gain server XP from battling or messaging.", 
    inline=False)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(    
    name="> /see_no_exp_channels", 
    value="See the channels where messaging (not battling) will not award you any server XP.", 
    inline=False)
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  return embed