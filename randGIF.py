import requests
import os
from pprint import pprint

#this py file has one function, it is to request and return the url of a gif based on the search_term; used mainly by the help pages and etc. THIS IS NOT USED BY THE .gif PREFIX COMMAND

def randgif(ARG):
  arg = ARG
  print (f"{arg}")
  search_term = arg
  lim = 1
  media_filter = "gif, tinygif"
  random = True
  SECRET_KEY = os.environ["TENOR_API_KEY"]
  ckey = "my_client_key"

  r = requests.get(
      f"https://tenor.googleapis.com/v2/search?q={search_term}&key={SECRET_KEY}&client_key={ckey}&limit={lim}&media_filter={media_filter}&random={random}")

  print(r.status_code)
  if r.status_code == 200:
    data = r.json()
    pprint(data)
    url = data["results"][0]["media_formats"]["gif"]["url"]
    print(url)
    return url
  else:
    data = None
