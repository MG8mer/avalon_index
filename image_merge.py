from PIL import Image
from io import BytesIO
import nextcord

#this python file is responsible for merging images together; this is mainly for the battle sequence and so the users have some sort of visual representation of the battle field and their health making the battles more fun 
#still haven't implemented into the bot yet

def overlay_img(bg, bar_R, bar_L):
  im_bar_R = Image.open(bar_R)
  im_bar_L = Image.open(bar_L)
  im_bg = Image.open(bg)

  # Scale down the health bar of R
  new_width = im_bar_R.width // 6
  new_height = im_bar_R.height // 6
  im_bar_R = im_bar_R.resize((new_width, new_height))

  new_width_L = im_bar_L.width // 6
  new_height_L = im_bar_L.height // 6
  im_bar_L = im_bar_L.resize((new_width_L, new_height_L))

  # Change the location to paste the scaled health bar
  left_R = 310
  top_R = 150

  left_L = 50
  top_L = 150

  # Create a new image as the result
  result = im_bg.copy()

  # Overlay the scaled health bar on top of the background at the new location
  result.paste(im_bar_R, (left_R, top_R), im_bar_R)
  result.paste(im_bar_L, (left_L, top_L), im_bar_L)

  # Save the merged image to a buffer
  img_byte_array = BytesIO()
  result.save(img_byte_array, format="PNG")
  img_byte_array.seek(0)

  # Return the file object
  return file