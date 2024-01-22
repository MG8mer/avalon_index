import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from image_merge import overlay_img

knight = (1, )
archer = (2, )
mage = (3, )

async def battle_page(interaction, member, hp_percentage_starter, hp_percentage_reciever, class_starter, class_reciever):   
  reciever_name = member.name
  starter_name = interaction.user.name
  print(f"{starter_name}, {reciever_name}")
  
  health_R = 'custom_assets/health_R_100.png'
  health_L = 'custom_assets/health_L_100.png'
  character_starter = None
  character_reciever = None

  if class_starter == knight:
    character_starter = 'custom_assets/knight_flipped.png'
  elif class_starter == archer:
    character_starter = 'custom_assets/archer_flipped.png'
  elif class_starter == mage:
    character_starter = 'custom_assets/mage_flipped.png'
    
  if class_reciever == knight:
    character_reciever = 'custom_assets/knight_final.png'
  elif class_reciever == archer:
    character_reciever = 'custom_assets/final_archer_1.png'
  elif class_reciever == mage:
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

  print(f"{character_starter}, {character_reciever}, {health_L}, {health_R}, {hp_percentage_starter}, {hp_percentage_reciever}")
  battle_byte_img = overlay_img('custom_assets/bg_purple_field1.png', health_R, health_L, character_reciever, character_starter, starter_name, reciever_name)
  file = nextcord.File(battle_byte_img, filename="battle_page.png")
  embed = Embed(title = "Battle Screen", color = nextcord.Color.blue())
  embed.set_image(url = "attachment://battle_page.png")
  await interaction.followup.send(embed = embed, file = file)