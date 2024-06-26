import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from image_merge import overlay_img
from nextcord.ext import commands

characters = {
  "knight": 1,
  "archer": 2,
  "mage": 3 
}


async def battle_page(interaction, member, hp_percentage_starter, hp_percentage_reciever, class_starter, class_reciever, startrand_mage, recieverand_mage, switch, crit_hit, hp_starter, hp_reciever, move, dmg):   
  reciever_name = member.name
  starter_name = interaction.user.name
  health_R = 'custom_assets/health_R_100.png'
  health_L = 'custom_assets/health_L_100.png'
  character_starter = None
  character_reciever = None

  if class_starter == characters["knight"]:
    character_starter = 'custom_assets/knight_flipped.png'
  elif class_starter == characters["archer"]:
    character_starter = 'custom_assets/archer_flipped.png'
  elif class_starter == characters["mage"]:
    if startrand_mage == 7:
      character_starter = 'custom_assets/mage_nerfed_flipped.png'
    else:
      character_starter = 'custom_assets/mage_flipped.png'

  if class_reciever == characters["knight"]:
    character_reciever = 'custom_assets/knight_final.png'
  elif class_reciever == characters["archer"]:
    character_reciever = 'custom_assets/final_archer_1.png'
  elif class_reciever == characters["mage"]:
    if recieverand_mage == 7:
      character_reciever = 'custom_assets/final_mage_nerfed_eE.png'
    else:
      character_reciever = 'custom_assets/mage_final_normal.png'

  if hp_percentage_starter <= 75 and hp_percentage_starter > 50:
    health_L = 'custom_assets/health_L_75.png'
  elif hp_percentage_starter <= 50 and hp_percentage_starter > 25:
    health_L = 'custom_assets/health_L_50.png'
  elif hp_percentage_starter <= 25 and hp_percentage_starter > 0:
    health_L = 'custom_assets/health_L_25.png'
  elif hp_percentage_starter <= 0:
    health_L = 'custom_assets/health_L_0.png'
    
  if hp_percentage_reciever <= 75 and hp_percentage_reciever > 50:
    health_R = 'custom_assets/health_R_75.png'
  elif hp_percentage_reciever <= 50 and hp_percentage_reciever > 25:
    health_R = 'custom_assets/health_R_50.png'
  elif hp_percentage_reciever <= 25 and hp_percentage_reciever > 0:
    health_R = 'custom_assets/health_R_25.png'
  elif hp_percentage_reciever <= 0:
    health_R = 'custom_assets/health_R_0.png'

  battle_byte_img = overlay_img('custom_assets/bg_purple_field1.png', health_R, health_L, character_reciever, character_starter, starter_name, reciever_name)
  file = nextcord.File(battle_byte_img, filename="battle_page.png")
  if switch == False:
    if dmg == 0:
      embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{member.mention} used the move **{move}**, but missed the attack and dealt **0** damage! \n{interaction.user.mention} still has an HP of ***{hp_starter}***\n {member.mention} has an HP of ***{hp_reciever}***")
      embed.set_image(url = "attachment://battle_page.png")
    elif crit_hit == 3:
      if hp_starter <= 0:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{member.mention} used the move **{move}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***\n {member.mention} has an HP of ***{hp_reciever}***")
        embed.set_image(url = "attachment://battle_page.png")
      else:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{member.mention} used the move **{move}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***\n {member.mention} has an HP of ***{hp_reciever}***")
        embed.set_image(url = "attachment://battle_page.png")
    else:
      if hp_starter <= 0:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{member.mention} used the move **{move}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has a depleted HP of ***0***\n {member.mention} has an HP of ***{hp_reciever}***")
        embed.set_image(url = "attachment://battle_page.png")
      else:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{member.mention} used the move **{move}**, dealing **{dmg*-1}** damage! \n{interaction.user.mention} now has an HP of ***{hp_starter}***\n {member.mention} has an HP of ***{hp_reciever}***")
        embed.set_image(url = "attachment://battle_page.png")
  elif switch == True:
    if dmg == 0:
      embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{interaction.user.mention} used the move **{move}**, but missed the attack and dealt **0** damage! \n{member.mention} still has an HP of ***{hp_reciever}***\n {interaction.user.mention} has an HP of ***{hp_starter}***")
      embed.set_image(url = "attachment://battle_page.png")
    elif crit_hit == 3:
       if hp_reciever <= 0:
         embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{interaction.user.mention} used the move **{move}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***\n {interaction.user.mention} has an HP of ***{hp_starter}***")
         embed.set_image(url = "attachment://battle_page.png")
       else:
         embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{interaction.user.mention} used the move **{move}**, but landed a *critical* hit and dealt **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***\n {interaction.user.mention} has an HP of ***{hp_starter}***")
         embed.set_image(url = "attachment://battle_page.png")
    else:
      if hp_reciever <= 0:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{interaction.user.mention} used the move **{move}**, dealing **{dmg*-1}** damage! \n{member.mention} now has a depleted HP of ***0***\n {interaction.user.mention} has an HP of ***{hp_starter}***")
        embed.set_image(url = "attachment://battle_page.png")
      else:
        embed = Embed(title = "Battle Screen", color = nextcord.Color.blue(), description = f"{interaction.user.mention} used the move **{move}**, dealing **{dmg*-1}** damage! \n{member.mention} now has an HP of ***{hp_reciever}***\n {interaction.user.mention} has an HP of ***{hp_starter}***")
        embed.set_image(url = "attachment://battle_page.png")
  battle_screen = await interaction.followup.send(embed = embed, file = file)
  return battle_screen