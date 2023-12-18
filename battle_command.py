import nextcord
import random
from nextcord.embeds import Embed
from nextcord import Interaction
import asyncio
import pick_move
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

class_evaluation_reciever = None
class_evaluation_starter = None
class_value_reciever = None
class_value_starter = None
battle_value = None
starter_hp_value = None
reciever_hp_value = None

async def battle(interaction: Interaction, member: nextcord.Member, start_rand):
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (interaction.user.id,))
      class_value_starter = await cursor.fetchone()
      await cursor.execute('SELECT class FROM users WHERE user_id = ?', (member.id,))
      class_value_reciever = await cursor.fetchone()
      class_evaluation_starter = str(class_value_starter[0]) + str(class_value_reciever[0])
      class_evaluation_reciever = str(class_value_reciever[0]) + str(class_value_starter[0])
      await cursor.execute('UPDATE battles SET battle = ?, starter_hp = ?, reciever_hp = ?, evaluation_starter = ?, evaluation_reciever = ? WHERE starter_id = ? AND reciever_id = ?', (1, health[class_value_starter[0]], health[class_value_reciever[0]], evaluation[class_evaluation_starter], evaluation[class_evaluation_reciever], interaction.user.id, member.id,))
      await cursor.execute('SELECT starter_hp FROM battles WHERE starter_id = ?', (interaction.user.id,))
      starter_hp_value = await cursor.fetchone()
      await cursor.execute('SELECT reciever_hp FROM battles WHERE reciever_id = ?', (member.id,))
      reciever_hp_value = await cursor.fetchone()
    await db.commit()
  switch = None
  switch_value = None
  turn = 0
  while starter_hp_value[0] >= 0 and reciever_hp_value[0] >= 0:
    # Below https://stackoverflow.com/questions/21837208/check-if-a-number-is-odd-or-even-in-python
    if turn == 0 or turn % 2 == 0:
      switch_value = await pick_move.move(interaction, member, start_rand, class_value_starter, class_value_reciever, switch)
    else:
      switch = await pick_move.move(interaction, member, start_rand, class_value_starter, class_value_reciever, switch_value)

    if switch_value or switch == None:
      break
    turn += 1
 
async def get_move(interaction: Interaction, member: nextcord.Member):
  global current_move
  
def get_battle_state():
  pass