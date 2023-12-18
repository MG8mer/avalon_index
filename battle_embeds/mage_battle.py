import nextcord
from nextcord.embeds import Embed
import nextcord.interactions  
import aiosqlite
from nextcord import Interaction

health = {
  1: 150,
  2: 75,
  3: 100
}

evaluation = {
  "11": "Normal",
  "22": "Normal",
  "33": "Normal",
  "12": "Weak",
  "13": "Strong",
  "21": "Strong",
  "23": "Weak",
  "31": "Weak",
  "32": "Strong",
}

attacks = {
  1: {
    "Sword Jab": {
      "Weak": -5,
      "Normal": -10,
      "Strong": -15
    },
    "Sword Slash": {
      "Weak": -10,
      "Normal": -20,
      "Strong": -30
    },
    "Dual Sword Attack": {
      "Weak": -40,
      "Nomral": -45,
      "Strong": -50,
    },
    "Sliced and Diced": {
      "Weak": -60,
      "Normal": -65,
      "Strong": -70,
    }
  },
  2: {
    "Weak Arrow": {
      "Weak": -7,
      "Normal": -12,
      "Strong": -15
    },
    "Piercing Shot": {
      "Weak": -20,
      "Normal": -25,
      "Strong": -35
    },
    "Triple Shot": {
      "Weak": -45,
      "Nomral": -50,
      "Strong": -60,
    },
    "Make it Rain": {
      "Weak": -80,
      "Normal": -90,
      "Strong": -100,
    }
  },
  3: {
  "Zap": {
    "Weak": -6,
    "Normal": -11,
    "Strong": -14
  },
  "Fireball": {
    "Weak": -15,
    "Normal": -25,
    "Strong": -32
  },
  "Arcane Mania": {
    "Weak": -42,
    "Nomral": -47,
    "Strong": -55,
  },
  "Biden Blast": {
    "Weak": -70,
    "Normal": -75,
    "Strong": -80,
  }
}

}



async def battle_embd(interaction: Interaction, member: nextcord.Member, switch):
  hp = None
  evaluation = None
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      if switch == False:
        await cursor.execute(f"SELECT starter_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone()
        await cursor.execute(f"SELECT evaluation_starter FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone()
      elif switch == True:
        await cursor.execute(f"SELECT reciever_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone()
        await cursor.execute(f"SELECT evaluation_reciever FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone()
    await db.commit()
  embed = Embed(   
    title = "Moves",
    description = "Pick from the avaliable moves!",
    color = nextcord.Color.purple())
  embed.add_field(    
    name="HP:", 
    value=str(hp[0]),
    inline=True)
  embed.add_field(
    name="Zap (Weak)",
    value=str(attacks[3]["Zap"][evaluation[0]]),
    inline=True)
  embed.add_field(
    name="Fireball (Normal)",
    value=str(attacks[3]["Fireball"][evaluation[0]]),
    inline=False)
  embed.add_field(
    name="Arcane Mania (Special)",
    value=str(attacks[3]["Arcane Mania"][evaluation[0]]),
    inline=False)
  embed.add_field(
    name="Biden Blast (Avalon's Blessing)",
    value=str(attacks[3]["Biden Blast"][evaluation[0]]),
    inline=False)
  embed.set_thumbnail(url="https://i.imgur.com/0DpJe0b.png")
  if switch == False:
    await interaction.user.send(embed=embed)
  elif switch == True:
    await member.send(embed=embed)