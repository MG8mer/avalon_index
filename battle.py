import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
import asyncio
import aiosqlite

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

USER_CLASS = ""


async def battle(interaction: Interaction, member: nextcord.Member):
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
      class_value_starter = await cursor.fetchone()
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
      class_value_reciever= await cursor.fetchone()
      class_evaluation = str(class_value_starter[0]) + str(class_value_reciever[0])
      await cursor.execute('INSERT INTO battles (battle, starter_id, starter_hp, reciever_id, reciever_hp, evaluation STRING) VALUES (?, ?, ?, ?, ?, ?)', (1, interaction.user.id, health[class_value_starter[0]], member.id, health[class_value_reciever[0]], evaluation[class_evaluation))
    await db.commit()
    
async def get_move(interaction: Interaction):
  pass

def get_battle_state():
  #return battle state back to battle function
  pass




