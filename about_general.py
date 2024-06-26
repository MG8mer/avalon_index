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
  embed = nextcord.Embed(title=f"__Starter Manual (pg. 1)__",
    description=f"This brief manual will provide a quick rundown on some components of Avalon Index, which mainly includes **__battling__** and **__levelling__**.", 
    colour=0x00b0f4)
  embed.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(name="**Battling Basics**",
    value="""Battling in Avalon Index starts with a player *(the starter)* requesting another player *(the reciever)* to battle. Upon the reciever's consent, (by responding `yes` or equivalent to the battle request) the battle will begin.""",
    inline=False)
  embed.add_field(
    name="",
    value="""Before the battle begins, a coin flip (50/50) will be used to determine which one of the players will start. Afterwards, an embed for the starting player will be sent in the channel, including information on the cooldowns of each of their moves, their damages, their hit chances, and buttons at the bottom of the embed for the starting player to select their move. After the player chooses the move, the embed will be deleted and a battle screen will be sent depicting a visual battlefield with both players and their HP bars. Additionally, the outcome of the move (i.e the amount of damage the move dealt, if it landed a critical hit, and if it killed the opponent) will be provided along with the HPs of both players.""",
    inline=False)
  embed.add_field(
    name="",
    value="""Afterwards, the same embed will be sent for the other player in the same channel, but for their class to select their move, where once they select it the previous battle screen will be deleted along with their embed and a new battle screen will be sent. The cycle will then continue where both players will continue to exchange moves until one of the players' HP is depleted, in which the other player will win the battle! That player will be rewarded XP for their global level and server level! *(More coming soon)*. """,
    inline=False)
  embed.add_field(
    name="**Specific Battling Details**",
    value="""Some extra info to note for battling can include: \n 1. Every move a player deals in a battle has a **20%** chance of landing a critical hit, which boosts the initial damage of an attack by **20%** as well! \n2. The cooldown and hit chance for each move type is as follows: \n a. Weak Attack: **0 Turn Cooldown; Hit Chance: 99.9%** *(no seriously)* \n b. Normal Attack: ** 1 Turn Cooldown (after first use); Hit Chance: 80%** \n c. Special Attack: **2 Turn Cooldown; Hit Chance: 50%** \n d. Avalon Blessing: **3 Cooldown; Hit Chance: 25%** \n3. For the first two turns of each player, they can forfeit the battle. However, neither player gains XP if either player forfeits, and this also applies if either player goes AFK for longer than 2 minutes. After those two turns, however, the two players are locked in and one must win the batte if they want their *juicy* XP.""",
    inline=False)
  embed.add_field(name="**Levelling**",
    value="Currently in Avalon Index, each player has two types of levels: \n \n1. Global Levels \n2. Server Levels \n \n**NOTE**: Both levels utilize the same mechanism for levelling, it's just that both levels are levelled up in different ways. Let XP that levels up a user's global level be called **global XP** and XP that levels up server levels be called **server XP**.",
    inline=False)
  embed.add_field(name="`Global`",
    value="A user's global level is levelled up **only** by battling other users and cannot be levelled up by messaging in a server. Global XP gained from battling is not boosted from boosted XP roles on a server (roles set by mods that earn more server XP for a specific server only through messaging). Additionally, you cannot gain level roles on the server (roles set by mods earned when reaching a particular server level on a server) based on if you level up your global level, and your global level will still level up even when you have a no XP role (roles set by mods that cannot earn server XP for a server by battling or messaging) on the server and even if you battle in a no XP channel (channels set by mods where **only** messaging will not earn any server XP for a server) on the server. **Global levels are reset when `/reset` is used**.",
    inline=True)
  embed.add_field(name="`Server`",
    value="A user will have multiple server levels and each will be different, in which each server level is based on each server the user plays Avalon Index/messages in, where server levels are levelled up by battling other users in the respective server and messaging in that same server. The amount of server XP earned to level up server levels by messaging (*not battling*) can be boosted by boosted XP roles set by mods on the server, and roles can be set to be earned on the server when reaching a particular server level. However, roles can be set in the server where if a user has them they will not be able to level up their server level in that server by battling or messaging, and channels can be set in the server where messaging in them (*not battling*) will not grant any server XP. Users can also compete to reach the top of a server's leaderboard by levelling their server level up as much as they can! **No server levels are reset after using `/reset`**.",
    inline=True)
  embed.set_thumbnail(url=f"{bot_avatar_url}")

  return embed