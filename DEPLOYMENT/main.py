import discord, os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('TOKEN')

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))

@bot.command(description="Have Parappa the Rapper rap what you rapped!")
async def parappa(ctx):
  try:
    await ctx.respond("testing")
  except:
     await ctx.respond("error")

bot.run(token)