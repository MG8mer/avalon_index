import nextcord
import nextcord.embeds
import nextcord.interactions
import randGIF

#this is the start page, the first page the players will see when they get started w the bot

async def start(interaction, bot_name, bot_avatar_url):
  botName=bot_name
  emoji = 'https://tenor.com/view/tower-defense-simulator-roblox-itzsweaking-mario-minecraft-gif-21237948'
  url = randGIF.randgif("GOOD LUCK RPG VIDEO GAME")
  embed = nextcord.Embed(title=f"**__Welcome to Avalon Index!__**",
    description=f"Hey {interaction.user.mention}! **__Avalon Index__** is a simple turn-based RPG game developed by **Hamzeus, Po, and Avash**. To get started, follow the steps below. We hope you enjoy!",
    colour=0x00b0f4)
  embed.set_author(name=botName,
    icon_url=bot_avatar_url)
  embed.add_field(name="**Pick Your Class**",
    value="You must pick **1** out of the **3** currently available classes to accompany you on your journey. Use ``.pick`` command once ready.",
    inline=False)
  embed.add_field(name="**Knight** `1`",
    value="The knight is the tankiest, **__close range__** class in the game.",
    inline=True)
  embed.add_field(name="**Archer** `2`",
    value="The archer has amazing and deadly **__long range__** capabilities but is the weakest",
    inline=True)
  embed.add_field(name="**Mage** `3`",
    value="The mage is a **__mid ranger__** class and lacks in both defence and damange",
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
  await interaction.response.defer()
  await interaction.followup.send(embed=embed)