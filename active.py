# Keeping bot active 24/7 when the code is running using flask(From Replit's article "Building a Discord bot with Python and Replit") (https://docs.replit.com/tutorials/python/build-basic-discord-bot-python)
#we are also using another website called uptimerobot to constantly send requests every few minutes to make sure the script doesn't stop as replit will stop any running script after a specific time

from flask import Flask, render_template
from threading import Thread

app = Flask(__name__)

@app.route('/')
def index():
    return "Alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def active():
    t = Thread(target=run)
    t.start()