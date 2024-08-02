import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from datetime import datetime
import randGIF

async def help(interaction, bot_name, bot_avatar_url):
  botName = bot_name
  bot_avatar_url = bot_avatar_url
  url = randGIF.randgif("HELP ME")
  embed = Embed(  
    title = f"**{botName}'s Help Menu (pg. 4)**", 
    description=f"All the commands for Avalon Index, including moderator and user ones! *For more info on global/server levels, see the General page of the `/avi_manual` command.* {interaction.user.mention}",
    color = nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(   
    name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(  
    name="/remove_level_role", 
    value="Remove a role that is awarded when a particular server level is reached on this server.",
    inline=True)
  embed.add_field(   
    name="> Syntax", 
    value="```\n/remove_level_role <level: a valid integer>\n```", 
    inline=True)
  embed.add_field(    
    name="Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="/remove_exp_boosted_role",
    value="Remove a role that gains extra server XP from messaging & battling on this server.",
    inline=True)
  embed.add_field(   
    name="> Syntax", 
    value="```\n/remove_exp_boosted_role <role: a role on this server>```\n", 
    inline=True)
  embed.add_field(    
    name="Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(    
    name="/remove_no_exp_channel", 
    value="Remove a channel on this server where server XP cannot be gained from messaging (not battling).", 
    inline=True)
  embed.add_field(    
    name="> Syntax", 
    value="```\n/remove_no_exp_channel <channel: a channel on this server>\n```", 
    inline=True)
  embed.add_field(    
    name="Permissions", 
    value="```\nA user must have the *Manage Channels* permission to use this command on this server.\n```", 
    inline=True)
  embed.add_field(    #blank embed to seperate
    name="",
    value="",
    inline=False)
  embed.add_field(   
    name="/remove_no_exp_role", 
    value="Remove a role that cannot gain server XP from battling or messaging on this server.", 
    inline=True)
  embed.add_field(    
    name="> Syntax", 
    value="```\n/remove_no_exp_role <role: a role on this server>\n```", 
    inline=True)
  embed.add_field(    
    name="Permissions", 
    value="```\nA user must have the *Manage Roles* permission to use this command on this server.\n```", 
    inline=True)
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  return embed