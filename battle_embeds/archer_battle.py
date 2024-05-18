import nextcord
from nextcord.embeds import Embed
import nextcord.interactions 
from nextcord import Interaction
import aiosqlite

# Useful source throughout: https://discordpy.readthedocs.io/en/stable/interactions/api.html

# Dicts to store class info:

# Class health
health = {
  1: 125,
  2: 75,
  3: 100
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


  

# Function to send an embed to the user when they use battle if they picked archer.
async def battle_embd(interaction: Interaction, member: nextcord.Member, switch, turn, starter_hp_value, reciever_hp_value, battle_screen):
  id_user = interaction.user.id 
  id_member = member.id
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      if switch == False:
        await cursor.execute('SELECT n_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        normal_c = await cursor.fetchone()
        await cursor.execute('SELECT s_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        special_c = await cursor.fetchone()
        await cursor.execute('SELECT ab_cooldown FROM cooldowns WHERE user_id = ?', (interaction.user.id,))
        avalonbless_c = await cursor.fetchone()
      elif switch == True:
        await cursor.execute('SELECT n_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        normal_c = await cursor.fetchone()
        await cursor.execute('SELECT s_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        special_c = await cursor.fetchone()
        await cursor.execute('SELECT ab_cooldown FROM cooldowns WHERE user_id = ?', (member.id,))
        avalonbless_c = await cursor.fetchone()
    await db.commit()


  # Create a class for two buttons (yes and no) like /reset.
  class RunStay(nextcord.ui.View):
    def __init__(self):
      super().__init__(timeout=3)
      self.value = None

    # For yes, delete the battle instance as a result of one of the belligerents running away.
    @nextcord.ui.button(label = 'Yes', style=nextcord.ButtonStyle.green) #yes button for ff
    async def y(self, button: nextcord.ui.Button, interaction: Interaction):
      async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
          await cursor.execute('SELECT battle FROM battles WHERE starter_id = ?', (interaction.user.id,))
          battle_check_one = await cursor.fetchone() # Check if the starter is the one who used /ff
          await cursor.execute('SELECT battle FROM battles WHERE reciever_id = ?', (interaction.user.id,))
          battle_check_two = await cursor.fetchone() # Check if the reciever is the one who used /ff
          if battle_check_one == (1,): # If the starter used /ff, use their id to delete the battle instance row.
            await cursor.execute('DELETE FROM battles WHERE starter_id = ?', (interaction.user.id,))
          elif battle_check_two == (1,):  # If the reciever used /ff, use their id to delete the battle instance row.
             await cursor.execute('DELETE FROM battles WHERE reciever_id = ?', (interaction.user.id,))
          await cursor.execute(f"DELETE FROM moves WHERE user_id = {interaction.user.id}")
          await cursor.execute(f"DELETE FROM moves WHERE opponent_id = {interaction.user.id}")
          await cursor.execute(f"DELETE FROM cooldowns WHERE user_id = {interaction.user.id}")
          await cursor.execute(f"DELETE FROM cooldowns WHERE opponent_id = {interaction.user.id}")
          await interaction.response.send_message(f"{interaction.user.mention} has run away from the battle!", ephemeral=False) # Inform both users that the person who used /ff ranaway from the bottle because ephemeral is false, so everyone sees the message, unlike when ephemeral is true and only the person who performed the interaction sees the message.
        await db.commit()
      self.value = True # Allow for the button to do something.
      self.stop() # After the button is pressed, stop the interaction.

    # TODO
    @nextcord.ui.button(label = 'No', style=nextcord.ButtonStyle.red) #no button for ff
    async def n(self, button: nextcord.ui.Button, interaction: Interaction):
      await interaction.response.send_message('The battle continues!', ephemeral=True) # Inform the user that the battle continues.
      self.value = False # This button being pressed will be as though nothing happened.
      self.stop() # After the button is pressed, stop the interaction.

  class ChooseFour(nextcord.ui.View):
    def __init__(self):
      super().__init__(timeout=120)
      self.value = None

    @nextcord.ui.button(label="FF", style=nextcord.ButtonStyle.red)
    async def ff(self, button: nextcord.ui.Button, interaction: Interaction):
      if switch == False and interaction.user.id != id_user:
          await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
      elif switch == True and interaction.user.id != id_member:
          await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
      else:
        view = RunStay()
        await interaction.response.send_message("Are you sure you want to forfeit this battle?", view=view, ephemeral=True)
        await view.wait()
        if view.value == None:
          await interaction.send("Request timed out.", ephemeral=True)
        elif view.value == True:
          self.value = "FF"
          self.stop()
    
    @nextcord.ui.button(label = "Weak Arrow", style=nextcord.ButtonStyle.blurple)
    async def weak(self, button: nextcord.ui.Button, interaction: Interaction):
        if switch == False and interaction.user.id != id_user:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        elif switch == True and interaction.user.id != id_member:
            await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
        else:
            move = "Weak Arrow"
            async with aiosqlite.connect("main.db") as db:
              async with db.cursor() as cursor:
                if switch == False:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,)) 
                elif switch == True:
                  await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
              await db.commit()
            self.value = True
            self.stop()
  
    if normal_c[0] == 0:
      @nextcord.ui.button(label = "Piercing Shot", style=nextcord.ButtonStyle.blurple)
      async def normal(self, button: nextcord.ui.Button, interaction: Interaction):
            if switch == False and interaction.user.id != id_user:
                await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
            elif switch == True and interaction.user.id != id_member:
                await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
            else:
                move = "Piercing Shot"
                async with aiosqlite.connect("main.db") as db:
                  async with db.cursor() as cursor:
                    if switch == False:
                      await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                    elif switch == True:
                      await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
                  await db.commit()
                self.value = True
                self.stop()
  
    if special_c[0] == 0:
       @nextcord.ui.button(label = "Triple Shot", style=nextcord.ButtonStyle.blurple)
       async def special(self, button: nextcord.ui.Button, interaction: Interaction):
              if switch == False and interaction.user.id != id_user:
                  await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
              elif switch == True and interaction.user.id != id_member:
                  await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
              else:
                    move = "Triple Shot"
                    async with aiosqlite.connect("main.db") as db:
                      async with db.cursor() as cursor:
                        if switch == False:
                          await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                        elif switch == True:
                          await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
                      await db.commit()
                    self.stop()
  
    if avalonbless_c[0] == 0:
      @nextcord.ui.button(label = "Make it Rain", style=nextcord.ButtonStyle.blurple)
      async def blessing(self, button: nextcord.ui.Button, interaction: Interaction):
          if switch == False and interaction.user.id != id_user:
              await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
          elif switch == True and interaction.user.id != id_member:
              await interaction.response.send_message("Buddy you can't choose their move for them!", ephemeral=True)
          else:
              move = "Make it Rain"
              async with aiosqlite.connect("main.db") as db:
                async with db.cursor() as cursor:
                  if switch == False:
                    await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (id_user, member.id, move, turn,))
                  elif switch == True:
                    await cursor.execute(f"INSERT INTO moves (user_id, opponent_id, move_used, turn_num) VALUES (?, ?, ?, ?)", (member.id, id_user, move, turn,))
                await db.commit()
              self.stop()
      
  view = ChooseFour()
  hp = None # Define hp
  evaluation = None # Define evaluation
  async with aiosqlite.connect("main.db") as db:
    async with db.cursor() as cursor:
      if switch == False: # If it's the starter's turn
        user = interaction.user
        await cursor.execute(f"SELECT starter_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone() # Get hp value of that user
        await cursor.execute(f"SELECT evaluation_starter FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone() # Get the evaluation of that user
      elif switch == True: # If it's the reciever's turn
        user = member
        await cursor.execute(f"SELECT reciever_hp FROM battles WHERE starter_id = {interaction.user.id}")
        hp = await cursor.fetchone()  # Get hp value of that user
        await cursor.execute(f"SELECT evaluation_reciever FROM battles WHERE starter_id = {interaction.user.id}")
        evaluation = await cursor.fetchone() # Get the evaluation of that user
    await db.commit()
  embed = Embed( # Title and description, indicating user to pick a move.
    title = f"{user} Moves",
    description = "",
    color = nextcord.Color.green())
  embed.add_field( # Field that shows hp.
    name="HP:", 
    value=str(hp[0]),
    inline=False)
  embed.add_field( # Field that shows the weak attack for that class and damage according the value of that user's evaluation.
    name="Weak Arrow (Weak) **No Cooldown**",
    value=str(attacks[2]["Weak Arrow"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the normal attack for that class and damage according the value of that user's evaluation.
    name=f"Piercing Shot (Normal) **Cooldown: {normal_c[0]}**",
    value=str(attacks[2]["Piercing Shot"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the special attack for that class and damage according the value of that user's evaluation.
    name=f"Triple Shot (Special) **Cooldown: {special_c[0]}**",
    value=str(attacks[2]["Triple Shot"][evaluation[0]]),
    inline=False)
  embed.add_field( # Field that shows the weak avalon blessing attack for that class and damage according the value of that user's evaluation.
    name=f"Make it Rain (Avalon's Blessing) **Cooldown: {avalonbless_c[0]}**",
    value=str(attacks[2]["Make it Rain"][evaluation[0]]),
    inline=False)            
  embed.set_thumbnail( # Shows image of archer.
    url="https://i.imgur.com/NcJsHO3.png"
  ) 
  if switch == False: # If it's the starter's turn, send the embed in their dm.
    message = await interaction.followup.send(embed=embed, view=view)
    await view.wait()
    if view.value is None:
      return
    elif view.value == "FF":
      return False
    await message.delete()
    if battle_screen != None:
      await battle_screen.delete()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {interaction.user.id}")
        move_final = await cursor.fetchone()
        if normal_c[0] == 0 and move_final[0] == "Piercing Shot":
          await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, interaction.user.id,))
        elif normal_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {interaction.user.id}')

        if special_c[0] == 0 and move_final[0] == "Triple Shot":
          await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, interaction.user.id,))
        elif special_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {interaction.user.id}')

        if avalonbless_c[0] == 0 and move_final[0] == "Make it Rain":
          await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, interaction.user.id,))
        elif avalonbless_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {interaction.user.id}')
      await db.commit()
      return move_final
  elif switch == True: # If it's the reciever's turn, send the embed in their dm.
    message = await interaction.followup.send(embed=embed, view=view)
    await view.wait()
    if view.value is None:
      return
    elif view.value == "FF":
      return False
    await message.delete()
    if battle_screen != None:
      await battle_screen.delete()
    async with aiosqlite.connect("main.db") as db:
      async with db.cursor() as cursor:
        await cursor.execute(f"SELECT move_used FROM moves WHERE turn_num = {turn} AND user_id = {member.id}")
        move_final = await cursor.fetchone()
        if normal_c[0] == 0 and move_final[0] == "Piercing Shot":
          await cursor.execute('UPDATE cooldowns SET n_cooldown = ? WHERE user_id = ?', (1, member.id,))
        elif normal_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET n_cooldown = {(normal_c[0] - 1)} WHERE user_id = {member.id}')

        if special_c[0] == 0 and move_final[0] == "Triple Shot":
          await cursor.execute('UPDATE cooldowns SET s_cooldown = ? WHERE user_id = ?', (2, member.id,))
        elif special_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET s_cooldown = {(special_c[0] - 1)} WHERE user_id = {member.id}')

        if avalonbless_c[0] == 0 and move_final[0] == "Make it Rain":
          await cursor.execute('UPDATE cooldowns SET ab_cooldown = ? WHERE user_id = ?', (3, member.id,))
        elif avalonbless_c[0] != 0:
          await cursor.execute(f'UPDATE cooldowns SET ab_cooldown = {(avalonbless_c[0] - 1)} WHERE user_id = {member.id}')
      await db.commit()
      return move_final
