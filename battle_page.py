import nextcord
from nextcord.embeds import Embed
import nextcord.interactions
from image_merge import overlay_img

async def battle_page(interaction, member, message, hp_percentage): 
  # if class_starter == 0  and class_reciever == 0:
    if hp_percentage == 100:
      battle_byte_img = overlay_img('custom_assets/bg_purple_field1.png', 'custom_assets/health_R_100.png', 'custom_assets/health_L_100.png', 'custom_assets/knight_final.png', 'custom_assets/knight_final.png')
      file = nextcord.File(battle_byte_img, filename="battle_page.png")
      embed = Embed(title = "Battle Screen", description = message, color = nextcord.Color.blue())
      embed.set_image(url = "attachment://battle_page.png")
      await interaction.response.defer()
      await interaction.followup.send(file = file, embed = embed)

    elif hp_percentage == 75:
    
    # await interaction.response.send_message(embed = embed, file=file)