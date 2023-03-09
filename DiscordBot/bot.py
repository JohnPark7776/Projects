import discord
from discord.ext import commands
import os
from Instagram_Link import start_this

default_prefix = '$'

def run_discord_bot():
  intents = discord.Intents.default()
  intents.message_content = True
  bot_client = commands.Bot(intents=intents, command_prefix=default_prefix)

  @bot_client.event
  async def on_ready():
    print(f'We have logged in as {bot_client}')


  @bot_client.command()
  async def ig(message, arg):
    ig_link = str(arg)
    try:
      response = await start_this(ig_link)
      for i in response:
        await message.channel.send(i)
    except Exception as e:
      print(e)
  
  @bot_client.command()
  async def prefix(message, arg):
    default_prefix = str(arg)
    bot_client.command_prefix = default_prefix
    await message.channel.send(f'The new prefix is now {default_prefix}.')

  with open ('C:/Users/SexyKoreanese/Desktop/key.txt') as key:
    temp = key.read()









  try:
    bot_client.run(temp)
  except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    os.system("restarter.py")
    os.system('kill 1')
