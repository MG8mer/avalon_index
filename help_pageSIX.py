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
    title = f"**{botName}'s Help Menu (pg. 6)**", 
    description=f"All the commands for Avalon Index, including moderator and user ones! *For more info on global/server levels, see the General page of the `/avi_manual` command.* {interaction.user.mention}",
    color = nextcord.Color.blurple(),
    timestamp=datetime.now())
  embed.set_author(   
    name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(  
    name="/set_levelup_channel", 
    value="Assign a channel on this server where level up embeds are sent.",
    inline=True)
  embed.add_field(   
    name="> Syntax", 
    value="```\n/set_levelup_channel <channel>\n```", 
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
    name="/reset_levelup_channel",
    value="Reset level up embeds to be sent in the channel where the battle/message caused the level up.",
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
    name="/levelup_config", 
    value="See leveling settings for this server.", 
    inline=True)
  embed.set_thumbnail(url=f"{url}")
  embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/SuXNrLh3RW0AAAAi/ebichu-help-me.gif")
  return embed