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
  embed = Embed(title = f"**{botName}'s Help Menu (pg. 5)**",
    description=f"All the commands for Avalon Index, including moderator and user ones! *For more info on global/server levels, see the General page of the `/avi_manual` command.* {interaction.user.mention}",
    colour=nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(name=botName, #author field
    icon_url=bot_avatar_url)
  embed.add_field(    
    name="/clear_level_roles", 
    value="Clear all the server levels associated with their respective role on this server.", 
    inline=True)
  embed.add_field(    
    name="> Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="/clear_exp_boosted_roles", 
    value="Clear all the server XP boosts from the applicable roles on this server.", 
    inline=True)
  embed.add_field(    
    name="> Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="/clear_no_exp_channels",
    value="Remove the no server XP restriction from all the channels that have it on this server.", 
    inline=True)
  embed.add_field(    
    name="> Permissions", 
    value="```\nA user must have the *Manage Channels* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(  
    name="",
    value="",
    inline=False)
  embed.add_field(    
    name="/clear_no_exp_roles", 
    value="Remove the no XP restriction from all roles that have it on this server.", 
    inline=True)
  embed.add_field(    
    name="> Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  return embed