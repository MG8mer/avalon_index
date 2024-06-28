import os
import nextcord
import random
from nextcord.embeds import Embed
from nextcord import Interaction
from nextcord.ext import commands
import asyncio
import pick_move
import asyncpg
import battle_page
from random import randint
from shared import role_designation

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

client = commands.Bot(command_prefix=".", intents = nextcord.Intents.all()) # Define client.

# Dicts to store class info: 

# Class health
health = {
  1: 150,
  2: 100,
  3: 125
}

# Battle evaluation:
  # Ex: 12; if a knight fights an archer it's weak for the knight.
  # Ex 2: 32: if a mage fights an archer, it's strong for the mage.
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

# Dict order:
  # Class
    # Attacks:
      # Damage dependent on evaluation.

attacks = {
  1: {
    "Sword Jab": {
      "Weak": -10,
      "Normal": -15,
      "Strong": -20
    },
    "Sword Slash": {
      "Weak": -15,
      "Normal": -25,
      "Strong": -35
    },
    "Dual Sword Attack": {
      "Weak": -30,
      "Normal": -45,
      "Strong": -60
    },
    "Sliced and Diced": {
      "Weak": -50,
      "Normal": -75,
      "Strong": -100
    }
  },
  2: {
    "Weak Arrow": {
      "Weak": -15,
      "Normal": -20,
      "Strong": -25
    },
    "Piercing Shot": {
      "Weak": -25,
      "Normal": -35,
      "Strong": -45
    },
    "Triple Shot": {
      "Weak": -50,
      "Normal": -70,
      "Strong": -90,
    },
    "Make it Rain": {
      "Weak": -85,
      "Normal": -125,
      "Strong": -150,
    }
  },
  3: {
  "Zap": {
    "Weak": -12,
    "Normal": -18,
    "Strong": -22
  },
  "Fireball": {
    "Weak": -22,
    "Normal": -32,
    "Strong": -42
  },
  "Arcane Mania": {
    "Weak": -45,
    "Normal": -65,
    "Strong": -80,
  },
  "Biden Blast": {
    "Weak": -75,
    "Normal": -100,
    "Strong": -125,
  }
}

}

# Define important variables to be used globally.
class_evaluation_reciever = None # Eval of reciever
class_evaluation_starter = None # Eval of strter
class_value_reciever = None # Class of reciever
class_value_starter = None # Class of starter
battle_value = None # If battle has been initiated 
starter_hp_value = None # hp of starter
reciever_hp_value = None # hp of reciever
hp_percentage_starter = None
hp_percentage_reciever = None

async def battle(interaction: Interaction, member: nextcord.Member, start_rand, db_pool):
  async with db_pool.acquire() as cursor:

    class_value_starter = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', interaction.user.id)
    class_value_reciever = await cursor.fetchval('SELECT class FROM users WHERE user_id = $1', member.id)
    class_evaluation_starter = str(class_value_starter) + str(class_value_reciever) # Concatenate strings of class values to see their evaluation according to the assigned dictionary.
    class_evaluation_reciever = str(class_value_reciever) + str(class_value_starter) # Concatenate strings of class values to see their evaluation according to the assigned dictionary.
    await cursor.execute('UPDATE battles SET battle = $1, starter_hp = $2, reciever_hp = $3, evaluation_starter = $4, evaluation_reciever = $5 WHERE starter_id = $6 AND reciever_id = $7', 1, health[class_value_starter], health[class_value_reciever], evaluation[class_evaluation_starter], evaluation[class_evaluation_reciever], interaction.user.id, member.id) # Update the battle row of both users, insertting values such as their health, evaluation determined by insertting the concatenated string above into the dict, and their ids.

    startrand_mage = None
    recieverand_mage = None
    if class_value_starter == 1:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", interaction.user.id, member.id, "Sword Jab", 0, "Sword Slash", 0, "Dual Sword Attack", 2, "Sliced and Diced", 3)
    elif class_value_starter == 2:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", interaction.user.id, member.id, "Weak Arrow", 0, "Piercing Shot", 0, "Triple Shot", 2, "Make it Rain", 3)
    elif class_value_starter == 3:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", interaction.user.id, member.id, "Zap", 0, "Fireball", 0, "Arcane Mania", 2, "Biden Blast", 3)
        startrand_mage = randint(1, 10)

    if class_value_reciever == 1:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", member.id, interaction.user.id, "Sword Jab", 0, "Sword Slash", 0, "Dual Sword Attack", 2, "Sliced and Diced", 3)
    elif class_value_reciever == 2:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", member.id, interaction.user.id, "Weak Arrow", 0, "Piercing Shot", 0, "Triple Shot", 2, "Make it Rain", 3)
    elif class_value_reciever == 3:
        await cursor.execute(f"INSERT INTO cooldowns (user_id, opponent_id, weak, w_cooldown, normal, n_cooldown, special, s_cooldown, avalon_blessing, ab_cooldown) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)", member.id, interaction.user.id, "Zap", 0, "Fireball", 0, "Arcane Mania", 2, "Biden Blast", 3)
        recieverand_mage = randint(1, 10)

    starter_hp_value = await cursor.fetchval('SELECT starter_hp FROM battles WHERE starter_id = $1', interaction.user.id)
    reciever_hp_value = await cursor.fetchval('SELECT reciever_hp FROM battles WHERE reciever_id = $1', member.id)

  switch = None # Define turns
  switch_value = None # Define another variable for turns
  turn = 0 # Turn num
  hp_starter = starter_hp_value 
  hp_reciever = reciever_hp_value
  dmg_msg = None
  battle_screen = None
  starter_av_blessing_hits = 0
  reciever_av_blessing_hits = 0
  starter_crit_num = 0
  reciever_crit_num = 0
  while hp_starter > 0 and hp_reciever > 0:
    # Below https://stackoverflow.com/questions/21837208/check-if-a-number-is-odd-or-even-in-python
    if turn == 0 or turn % 2 == 0: # if turn is even, define switch_value, insertting switch into the move function in the pick_move file to return switch later and await whosever turn it is to pick a move.
      try:
        switch_value, dmg, move, crit_hit, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits = await pick_move.move(
          interaction, member, start_rand, startrand_mage, recieverand_mage, class_value_starter, class_value_reciever,
          starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch, turn,
          battle_screen, db_pool, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits)
      except TypeError:
        return
      else:
        async with db_pool.acquire() as cursor:
          if switch_value == True:
            hp_reciever += (dmg)
            await cursor.execute(f'UPDATE battles SET reciever_hp = {hp_reciever}')
            hp_percentage_starter = (hp_starter/starter_hp_value)*100
            hp_percentage_reciever = (hp_reciever/reciever_hp_value)*100
          elif switch_value == False:
            hp_starter += (dmg)
            await cursor.execute(f'UPDATE battles SET starter_hp = {hp_starter}') 
            hp_percentage_starter = (hp_starter/starter_hp_value)*100
            hp_percentage_reciever = (hp_reciever/reciever_hp_value)*100

        battle_screen = await battle_page.battle_page(interaction, member, hp_percentage_starter, hp_percentage_reciever, class_value_starter, class_value_reciever, startrand_mage, recieverand_mage, switch_value, crit_hit, hp_starter, hp_reciever, move, dmg)
        turn += 1

    else:  # if turn is odd, define switch, insertting switch_value into the move function in the pick_move file to return switch later and await whosever turn it is to pick a move.
      try:
        switch, dmg, move, crit_hit, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits = await pick_move.move(interaction, member, start_rand, startrand_mage, recieverand_mage, class_value_starter, class_value_reciever, starter_hp_value, reciever_hp_value, class_evaluation_starter, class_evaluation_reciever, switch_value, turn, battle_screen, db_pool, starter_crit_num, reciever_crit_num, starter_av_blessing_hits, reciever_av_blessing_hits)
      except TypeError:
        return
      else:
        async with db_pool.acquire() as cursor:
          if switch == True:
            hp_reciever += (dmg)
            await cursor.execute(f'UPDATE battles SET reciever_hp = {hp_reciever}')
            hp_percentage_starter = (hp_starter/starter_hp_value)*100
            hp_percentage_reciever = (hp_reciever/reciever_hp_value)*100
          elif switch == False:
            hp_starter += (dmg)
            await cursor.execute(f'UPDATE battles SET starter_hp = {hp_starter}') 
            hp_percentage_starter = (hp_starter/starter_hp_value)*100
            hp_percentage_reciever = (hp_reciever/reciever_hp_value)*100

        battle_screen = await battle_page.battle_page(interaction, member, hp_percentage_starter, hp_percentage_reciever, class_value_starter, class_value_reciever, startrand_mage, recieverand_mage, switch, crit_hit, hp_starter, hp_reciever, move, dmg)
        turn += 1

    if starter_hp_value == None or reciever_hp_value == None: # If the row has been deleted in pick_move, making these value none due to returning nothing, break the loop, ending the battle. 
      break
 # Add 1 to the turn count to cycle through the loop another time if its condition is still true, being that both players' health points are above 0.
  if hp_starter <= 0 or hp_reciever <= 0:
    async with db_pool.acquire() as cursor:

      await cursor.execute('DELETE FROM battles WHERE starter_id = $1', interaction.user.id)
      await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id} AND opponent_id = {member.id}")                 
      await cursor.execute(f"DELETE FROM moves WHERE user_id = {member.id} AND opponent_id = {interaction.user.id}")
      await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
      await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {member.id}")
    if hp_starter <= 0:
      server_no_exp = False
      no_exp_role = None
      server_boost_exp = False
      boosted_exp_role = None
      async with db_pool.acquire() as cursor:
        no_roles = await cursor.fetch("SELECT role_id FROM no_exp_roles WHERE guild_id = $1", interaction.guild_id)
      if no_roles != []:
          formatted_roles = []
          user_roles = [role.id for role in member.roles if role.name != "@everyone"]
          for id_role in no_roles:
            formatted_roles.append(id_role['role_id'])

          for roles in user_roles:
            if roles in formatted_roles:
              server_no_exp = True
              no_exp_role = nextcord.utils.get(interaction.guild.roles, id=roles) 

      if server_no_exp is False:
        async with db_pool.acquire() as cursor:
          boosted_roles = await cursor.fetch("SELECT role_id FROM exp_boosted_roles WHERE guild_id = $1", interaction.guild_id)
        if boosted_roles != []:
            formatted_roles = []
            user_roles = [role.id for role in member.roles if role.name != "@everyone"]
            for id_role in boosted_roles:
              formatted_roles.append(id_role['role_id'])

            boosted_exp_roles = []

            for roles in user_roles:
              if roles in formatted_roles:
                boosted_exp_roles.append(roles)

            if boosted_exp_roles != []:
              boost_percents = []
              async with db_pool.acquire() as cursor:
                for role_id in boosted_exp_roles:
                    boost_val = await cursor.fetchval(
                        f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {role_id} AND guild_id = {interaction.guild_id}")
                    boost_percents.append((role_id, boost_val))

              boost_percents.sort(key=lambda x: x[1], reverse=True)
              boosted_exp_roles = [role_id for role_id, _ in boost_percents]

              async with db_pool.acquire() as cursor:
                 boost_val = await cursor.fetchval(f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {boosted_exp_roles[0]} AND guild_id = {interaction.guild_id}")

              boosted_exp_role = nextcord.utils.get(interaction.guild.roles, id=boosted_exp_roles[0])
              server_boost_exp = True

      if recieverand_mage == 7:
        wildcard_mage_bonus = 25
      else:
        wildcard_mage_bonus = 0
      base_score = randint(50, 100)
      hp_bonus = round((hp_reciever/reciever_hp_value)*100)
      crit_bonus = reciever_crit_num*10
      av_blessing_bonus = reciever_av_blessing_hits*5
      battle_score=base_score+hp_bonus+crit_bonus+av_blessing_bonus+wildcard_mage_bonus
      async with db_pool.acquire() as cursor:
        global_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM global_levels WHERE user_id = {member.id}")
        server_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM server_levels WHERE user_id = {member.id} AND guild_id = {interaction.guild_id}")

      if global_result is None: 
        async with db_pool.acquire() as cursor:
          exp_needed = round(100*(pow(1, 1.1)))
          await cursor.execute(f"INSERT INTO global_levels (user_id, exp, level, exp_needed) VALUES ({member.id}, 0, 0, {exp_needed})")

      if server_result is None: 
        if server_no_exp == False:
          async with db_pool.acquire() as cursor:
            exp_needed = round(100*(pow(1, 1.1)))
            await cursor.execute(f"INSERT INTO server_levels (user_id, guild_id, exp, level, exp_needed) VALUES ({member.id}, {interaction.guild_id}, 0, 0, {exp_needed})")

      async with db_pool.acquire() as cursor:
        global_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM global_levels WHERE user_id = {member.id}")
        if server_no_exp == False:
          server_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM server_levels WHERE user_id = {member.id} AND guild_id = {interaction.guild_id}")

      global_exp = global_result[0]
      global_lvl = global_result[1]
      global_exp_needed = global_result[2]
      global_exp += battle_score
      async with db_pool.acquire() as cursor:
        await cursor.execute(f"UPDATE global_levels SET exp = {global_exp} WHERE user_id = {member.id}")
      while global_exp >= global_exp_needed: 
          global_lvl += 1
          exp_surplus = global_exp - global_exp_needed
          global_exp_needed = round(100*(pow((global_lvl+1), 1.1))) 
          async with db_pool.acquire() as cursor:
            await cursor.execute(f"UPDATE global_levels SET exp = {exp_surplus}, level = {global_lvl}, exp_needed = {global_exp_needed} WHERE user_id = {member.id}")
          global_exp = exp_surplus
          if global_exp >= global_exp_needed:
            pass
          else:
            embed = nextcord.Embed(title=f"**__Congratulations!__**",
              description=f"You have reached level {global_lvl} on **__Avalon Index!__**",
              colour=0x00b0f4)
            embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
            embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
            await member.send(embed=embed)

      if server_no_exp == False:
        server_exp = server_result[0]
        server_lvl = server_result[1]
        server_exp_needed = server_result[2]
        if server_boost_exp is True:
          new_battle_score = round(battle_score * ((boost_val/100) + 1))
          server_exp += new_battle_score
        else:
          server_exp += battle_score

        async with db_pool.acquire() as cursor:
          await cursor.execute(f"UPDATE server_levels SET exp = {server_exp} WHERE user_id = {member.id} AND guild_id = {interaction.guild_id} ")
        while server_exp >= server_exp_needed: 
            server_lvl += 1
            exp_surplus = server_exp - server_exp_needed
            server_exp_needed = round(100*(pow((server_lvl+1), 1.1)))
            async with db_pool.acquire() as cursor:
              await cursor.execute(f"UPDATE server_levels SET exp = {exp_surplus}, level = {server_lvl}, exp_needed = {server_exp_needed} WHERE user_id = {member.id} AND guild_id = {interaction.guild_id}") 
            server_exp = exp_surplus
            if server_exp >= server_exp_needed:
              pass
            else:
              embed = nextcord.Embed(title=f"**__Congratulations!__**",
                description=f"You have reached level {server_lvl} on the **__{interaction.guild}__** server!",
                colour=0x00b0f4)
              embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
              embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
              await member.send(embed=embed)
              await role_designation(member, member.id, interaction.guild, interaction.guild_id, interaction.channel, server_lvl, db_pool)

      if server_boost_exp is True:
        result_battle = Embed(   
          title = "Battle Results",
          description = f"The battle has concluded and {member.mention} has won!",
          color = nextcord.Color.blue())
        result_battle.add_field(
          name="Server XP Boost",
          value=f"The **{boosted_exp_role}** will boost your battle XP for your server XP (not global) by **{boost_val}%!**",
          inline=False)
        result_battle.add_field(    
          name="Score Breakdown", 
          value=f">**__Base XP__**: +{base_score} \n >HP Bonus: +{hp_bonus} \n >Crit Bonus: +{crit_bonus} \n >Avalon Blessing Bonus: +{av_blessing_bonus} \n >Wilcard Mage Bonus: +{wildcard_mage_bonus} \n \n  **__Total XP (Global)__**: {battle_score} \n **__Total XP (Server)__**: {new_battle_score}", 
          inline=False)
      else:
        result_battle = Embed(   
          title = "Battle Results",
          description = f"The battle has concluded and {member.mention} has won!",
          color = nextcord.Color.blue())
        result_battle.add_field(
          name="Server XP Boost",
          value='*You have no roles to boost your battle XP gained for your server level, or you have a no XP role on this server nullifying your XP boost from your boosted XP role on this server.*',
          inline=False)
        result_battle.add_field(    
          name="Score Breakdown", 
          value=f">**__Base XP__**: +{base_score} \n >HP Bonus: +{hp_bonus} \n >Crit Bonus: +{crit_bonus} \n >Avalon Blessing Bonus: +{av_blessing_bonus} \n >Wilcard Mage Bonus: +{wildcard_mage_bonus} \n \n **__Total XP__**: {battle_score}", 
          inline=False)
        if server_no_exp == True:
          result_battle.set_footer(text = f"NOTE: You have gained no XP on {interaction.guild} as you have the {no_exp_role} role, which cannot gain any XP on this server.")
      await interaction.followup.send(embed=result_battle)
    elif hp_reciever <= 0:
      server_no_exp = False
      no_exp_role = None
      server_boost_exp = False 
      boosted_exp_role = None 
      async with db_pool.acquire() as cursor:
        no_roles = await cursor.fetch("SELECT role_id FROM no_exp_roles WHERE guild_id = $1", interaction.guild_id)
      if no_roles != []:
          formatted_roles = []
          user_roles = [role.id for role in interaction.user.roles if role.name != "@everyone"]
          for id_role in no_roles:
            formatted_roles.append(id_role['role_id'])

          for roles in user_roles:
            if roles in formatted_roles:
              server_no_exp = True
              no_exp_role = nextcord.utils.get(interaction.guild.roles, id=roles)

      if server_no_exp is False:
        async with db_pool.acquire() as cursor:
          boosted_roles = await cursor.fetch("SELECT role_id FROM exp_boosted_roles WHERE guild_id = $1", interaction.guild_id)
        if boosted_roles != []:
            formatted_roles = []
            user_roles = [role.id for role in interaction.user.roles if role.name != "@everyone"]
            for id_role in boosted_roles:
              formatted_roles.append(id_role['role_id'])

            boosted_exp_roles = []

            for roles in user_roles:
              if roles in formatted_roles:
                boosted_exp_roles.append(roles)

            if boosted_exp_roles != []:
              boost_percents = []
              async with db_pool.acquire() as cursor:
                for role_id in boosted_exp_roles:
                    boost_val = await cursor.fetchval(
                        f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {role_id} AND guild_id = {interaction.guild_id}")
                    boost_percents.append((role_id, boost_val))
              boost_percents.sort(key=lambda x: x[1], reverse=True)

              boosted_exp_roles = [role_id for role_id, _ in boost_percents]

              async with db_pool.acquire() as cursor:
                 boost_val = await cursor.fetchval(f"SELECT boost_percent FROM exp_boosted_roles WHERE role_id = {boosted_exp_roles[0]} AND guild_id = {interaction.guild_id}")

              boosted_exp_role = nextcord.utils.get(interaction.guild.roles, id=boosted_exp_roles[0])
              server_boost_exp = True

      if startrand_mage == 7:
        wildcard_mage_bonus = 25
      else:
        wildcard_mage_bonus = 0
      base_score = randint(50, 100)
      hp_bonus = round((hp_starter/starter_hp_value)*100)
      crit_bonus = starter_crit_num*10
      av_blessing_bonus = starter_av_blessing_hits*5
      battle_score=base_score+hp_bonus+crit_bonus+av_blessing_bonus+wildcard_mage_bonus
      async with db_pool.acquire() as cursor:
        global_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM global_levels WHERE user_id = {interaction.user.id}")
        server_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM server_levels WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild_id}")

      if global_result is None: 
          async with db_pool.acquire() as cursor:
            exp_needed = round(100*(pow(1, 1.1)))
            await cursor.execute(f"INSERT INTO global_levels (user_id, exp, level, exp_needed) VALUES ({interaction.user.id}, 0, 0, {exp_needed})")

      if server_result is None: 
        if server_no_exp == False:
          async with db_pool.acquire() as cursor:
            exp_needed = round(100*(pow(1, 1.1)))
            await cursor.execute(f"INSERT INTO server_levels (user_id, guild_id, exp, level, exp_needed) VALUES ({interaction.user.id}, {interaction.guild_id}, 0, 0, {exp_needed})")

      async with db_pool.acquire() as cursor:
        global_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM global_levels WHERE user_id = {interaction.user.id}")
        if server_no_exp == False:
            server_result = await cursor.fetchrow(f"SELECT exp, level, exp_needed FROM server_levels WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild_id}")

      global_exp = global_result[0]
      global_lvl = global_result[1]
      global_exp_needed = global_result[2]
      global_exp += battle_score
      async with db_pool.acquire() as cursor:
        await cursor.execute(f"UPDATE global_levels SET exp = {global_exp} WHERE user_id = {interaction.user.id}")
      while global_exp >= global_exp_needed: 
          global_lvl += 1
          exp_surplus = global_exp - global_exp_needed
          global_exp_needed = round(100*(pow((global_lvl+1), 1.1))) 
          async with db_pool.acquire() as cursor:
            await cursor.execute(f"UPDATE global_levels SET exp = {exp_surplus}, level = {global_lvl}, exp_needed = {global_exp_needed} WHERE user_id = {interaction.user.id}")
          global_exp = exp_surplus
          if global_exp >= global_exp_needed:
            pass
          else:
            embed = nextcord.Embed(title=f"**__Congratulations!__**",
              description=f"You have reached level {global_lvl} on **__Avalon Index!__**",
              colour=0x00b0f4)
            embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
            embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
            await interaction.user.send(embed=embed)

      if server_no_exp == False:
        server_exp = server_result[0]
        server_lvl = server_result[1]
        server_exp_needed = server_result[2]

        if server_boost_exp is True:
          new_battle_score = round(battle_score * ((boost_val/100) + 1))
          server_exp += new_battle_score
        else:
          server_exp += battle_score

        async with db_pool.acquire() as cursor:
          await cursor.execute(f"UPDATE server_levels SET exp = {server_exp} WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild_id}")
        while server_exp >= server_exp_needed: 
            server_lvl += 1
            exp_surplus = server_exp - server_exp_needed
            server_exp_needed = round(100*(pow((server_lvl+1), 1.1)))
            async with db_pool.acquire() as cursor:
              await cursor.execute(f"UPDATE server_levels SET exp = {exp_surplus}, level = {server_lvl}, exp_needed = {server_exp_needed} WHERE user_id = {interaction.user.id} AND guild_id = {interaction.guild_id}") 
            server_exp = exp_surplus
            if server_exp >= server_exp_needed:
              pass
            else:
              embed = nextcord.Embed(title=f"**__Congratulations!__**",
                description=f"You have reached level {server_lvl} on the **__{interaction.guild}__** server!",
                colour=0x00b0f4)
              embed.set_thumbnail(url="https://cdn3.emoji.gg/emojis/5416-hollowpeped.gif")
              embed.set_footer(text = "Via Tenor", icon_url = "https://media.tenor.com/PeRI5dkeLFkAAAAi/tower-defense-simulator-roblox.gif")
              await interaction.user.send(embed=embed)
              await role_designation(interaction.user, interaction.user.id, interaction.guild, interaction.guild_id, interaction.channel, server_lvl, db_pool)

      if server_boost_exp is True:
        result_battle = Embed(   
          title = "Battle Results",
          description = f"The battle has concluded and {interaction.user.mention} has won!",
          color = nextcord.Color.blue())
        result_battle.add_field(
          name="Server XP Boost",
          value=f"The **{boosted_exp_role}** will boost your battle XP for your server XP (not global) by **{boost_val}%!**",
          inline=False)
        result_battle.add_field(    
          name="Score Breakdown", 
          value=f">**__Base XP__**: +{base_score} \n >HP Bonus: +{hp_bonus} \n >Crit Bonus: +{crit_bonus} \n >Avalon Blessing Bonus: +{av_blessing_bonus} \n >Wilcard Mage Bonus: +{wildcard_mage_bonus} \n \n  **__Total XP (Global)__**: {battle_score} \n **__Total XP (Server)__**: {new_battle_score}", 
          inline=False)
      else:
        result_battle = Embed(   
          title = "Battle Results",
          description = f"The battle has concluded and {interaction.user.mention} has won!",
          color = nextcord.Color.blue())
        result_battle.add_field(
          name="Server XP Boost",
          value='*You have no roles to boost your battle XP gained for your server level, or you have a no XP role on this server nullifying your XP boost from your boosted XP role on this server.*',
          inline=False)
        result_battle.add_field(    
          name="Score Breakdown", 
          value=f">**__Base XP__**: +{base_score} \n >HP Bonus: +{hp_bonus} \n >Crit Bonus: +{crit_bonus} \n >Avalon Blessing Bonus: +{av_blessing_bonus} \n >Wilcard Mage Bonus: +{wildcard_mage_bonus} \n \n **__Total XP__**: {battle_score}", 
          inline=False)
        if server_no_exp == True:
          result_battle.set_footer(text = f"NOTE: You have gained no XP on {interaction.guild} as you have the {no_exp_role} role, which cannot gain any XP on this server.")
      await interaction.followup.send(embed=result_battle)