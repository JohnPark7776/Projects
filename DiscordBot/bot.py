import discord
from discord.ext import commands
from Instagram_Link import start_this
from io import BytesIO

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
      """Prints out Instagram Img from post

      Args:
          message (_discord_): {default_prefix}ig
          arg (_discord_): Ig post URL
      """
      ig_link = str(arg)
      try:
          response = await start_this(ig_link)
          temp_file = []
          for num, output in enumerate(response):
            if response[output] == 'img':
              filename = f"image{num}.jpg"
              temp_file.append(discord.File(BytesIO(output), filename=filename))
            elif response[output] == 'vid':
              filename = f"video{num}.mp4"
              temp_file.append(discord.File(BytesIO(output), filename=filename))
          await message.channel.send(files=temp_file)
      except Exception as e:
          print(e)
  
  @bot_client.command()
  async def prefix(message, arg):
    """Changes the prefix

    Args:
        message (_discord_): {default_prefix}prefix
        arg (_discord_): New Prefix
    """
    default_prefix = str(arg)
    bot_client.command_prefix = default_prefix
    await message.channel.send(f'The new prefix is now {default_prefix}.')

  @bot_client.command()
  async def quit(message):
    """Turns off the bot

    Args:
        message (_discord_): Client.close()
    """
    bot_client.close()




  with open ('C:/Users/SexyKoreanese/Desktop/key.txt') as key:
    temp = key.read()

  bot_client.run(temp)

