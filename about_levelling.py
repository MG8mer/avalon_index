import os
import nextcord
import nextcord.embeds
import nextcord.interactions
from nextcord import Interaction
from nextcord.ext import commands
import asyncpg
import randGIF
from datetime import datetime


async def about(interaction: Interaction, bot_name, bot_avatar_url):
  botName=bot_name
  bot_avatar_url = bot_avatar_url
  embed = nextcord.Embed(title=f"__Starter Manual (pg. 2)__",
    colour=0x00b0f4)
  embed.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(name="__Levelling__",
    value="",
    inline=False)
  embed.add_field(name="",
    value="Currently in Avalon Index, each player has two types of levels: \n \n1. Global Levels \n2. Server Levels \n \n**NOTE**: Both levels utilize the same mechanism for levelling, it's just that both levels are levelled up in different ways. Let XP that levels up a user's global level be called **global XP** and XP that levels up server levels be called **server XP**. \n \n *Please note that in order to earn global XP/server XP for ANY server, `/start` MUST be used.*",
    inline=False)
  embed.add_field(name="`Global`",
    value="A user's global level will be their centralized level on Avalon index in every server. Global XP can only be earned by battling users on __any server__ and cannot be earned via messaging. Additionally, global XP earned from battling is not boosted from *boosted XP roles* (roles on a server that boost server XP earned from messaging and battling) on a particular server, and global XP can be obtained even if a user has a *no XP role* on a server (roles on a server that prevent a user from earning server XP from battling and messaging) and even if a user battles in a *no XP channel* on a server (channels where server XP cannot be earned from messaging (not battling)) or both. Lastly, *level roles* (roles on a server earned when reaching a specific server level) CANNOT be earned based on global level.",
    inline=True)
  embed.add_field(name="`Server`",
    value="A user will have multiple server levels for each server they message in and play Avalon Index in. Server XP for a particular server can be earned by messaging or battling on that server. Additonally, server XP earned from messaging or battling can be boosted from *boosted XP roles* on a server by a certain percentage set by mods on a server for a specific role. If a user has a *no XP role* on a server, they will not be able to earn server XP from battling or messaging, even if they have a *boosted XP role*, and by that same nature the boost from a XP boosted will be nullified. *No XP channels* can also be set on a server, where messaging in them won't grant any server XP, but you can still battle and gain server XP in them. A user with a *no XP role* won't be able to earn server XP from messaging or battling in a *no XP channel*.",
    inline=True)
  embed.add_field(name="`Server (cont'd)`",
    value="If a user messages/battles in a server with multiple *XP boosted roles*, the bot will use the role that has the highest XP boost. \n \n Lastly, *level roles* can be set on a server to be earned when reaching a specific server level on a server.",
    inline=False)
  embed.add_field(name="`Messaging for XP`",
    value="After a user uses `/start`, they will be able to level up their server level for specific servers by messaging. Everytime a user messages, they will be able to gain a *base amount* of **5-10 XP** (randomly chosen), with a **60 second cooldown** between messages for earning XP. \n \n If a user sends a message that is longer than 10 words, their base XP will be increased by **20%**, and afterwards if a user has a *XP boosted role*, that will then be applied then __afterwards__.",
    inline=False)
  embed.add_field(name="`Battling for XP`",
    value="""As mentioned earlier, users can battle other users to gain global & server XP. \n \n Here's how XP gained from battling works: \n \n - Base XP: 50-100 (randomly chosen). \n- HP Bonus: +1 XP for every % HP left. \n- Crit Bonus: +10 XP for every critical hit. \n- Avalon Blessing Bonus: +5 XP for every Avalon Blessing attack hit. \n- Wildcard Mage Bonus: +25 XP if the user got the wildcard variant of the mage (when playing mage) and still managed to win.
""",
    inline=False)
  embed.add_field(name="`Mod Levelling Commands`",
    value="""On Avalon Index exist many commands related to levelling. For more info on them, see pages `3-5` on `/help`. Here's some things to keep in mind, though: \n \n Level roles can be assigned to roles that are already *EITHER* *no XP roles* OR *XP boosted roles*, not both because of the following: \n \n - When assigning a *XP boosted role* on a server, the role CANNOT already be a *no XP role* (for logical reasons). \n \n- By the same logic, you cannot assign a no XP role to a role that is already a XP boosted role.""",
    inline=False)
  embed.set_thumbnail(url=f"{bot_avatar_url}")

  return embed