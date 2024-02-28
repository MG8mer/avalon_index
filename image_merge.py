#this python file is responsible for merging images together; this is mainly for the battle sequence and so the users have some sort of visual representation of the battle field and their health making the battles more fun 
#still haven't implemented into the bot yet

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from io import BytesIO
import nextcord

def overlay_img(bg, bar_R, bar_L, starter, reciever, starter_name, reciever_name):
  im_bar_R = Image.open(bar_R)
  im_bar_L = Image.open(bar_L)
  im_starter = Image.open(starter)
  im_reciever = Image.open(reciever)
  im_bg = Image.open(bg)

  # Resizing images
  new_width = im_bar_R.width // 6
  new_height = im_bar_R.height // 6
  im_bar_R = im_bar_R.resize((new_width, new_height))

  new_width_L = im_bar_L.width // 6
  new_height_L = im_bar_L.height // 6
  im_bar_L = im_bar_L.resize((new_width_L, new_height_L))

  new_width_ST = im_starter.width // 2
  new_height_ST = im_starter.height // 2
  im_bar_ST = im_starter.resize((new_width_ST, new_height_ST))

  new_width_RC = im_reciever.width // 2
  new_height_RC = im_reciever.height // 2
  im_bar_RC = im_reciever.resize((new_width_RC, new_height_RC))

  # Setting location
  left_R = 323
  top_R = 150

  left_L = 30
  top_L = 150

  left_ST = 337
  top_ST = 83

  left_RC = 78
  top_RC = 83

  # Create a new image called result, a copy of the bg
  result = im_bg.copy()
  draw = ImageDraw.Draw(result)
  font = ImageFont.truetype("custom_assets/built titling bd.otf", 15)
  draw.text((100,172), starter_name, (255,255,255), anchor = "lt", font=font, stroke_width = 2, stroke_fill = (0,0,0))
  draw.text((378, 178), reciever_name, (255,255,255), anchor = "rm", font=font, stroke_width = 2, stroke_fill = (0,0,0))

  # Overlay the scaled health bar and characters onto copy of the bg
  result.paste(im_bar_R, (left_R, top_R), im_bar_R)
  result.paste(im_bar_L, (left_L, top_L), im_bar_L)
  result.paste(im_bar_ST, (left_ST, top_ST), im_bar_ST)
  result.paste(im_bar_RC, (left_RC, top_RC), im_bar_RC)

  # Save the merged image to a buffer
  result.save('merged_image.png', format='PNG')
  img_byte_array = BytesIO()
  result.save(img_byte_array, format="PNG")
  img_byte_array.seek(0)

  # Return the file object
  return img_byte_array
