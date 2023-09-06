import discord, os
from discord import Option
from dotenv import load_dotenv
from parappa import repeat

# Getting token from .env file
load_dotenv()
token = os.getenv('TOKEN')

bot = discord.Bot()

# Bot initialization
@bot.event
async def on_ready():
    print("Bot {0.user} is ready!".format(bot))

# Slash command: Parappa repeats user message from his perspective
@bot.command(description="Have Parappa the Rapper rap what you rapped!")
async def parappa(ctx,*, rap: Option(str, "Enter your rap, dawg! ", required=True)):
  try:
    RptMsg = repeat(rap)
    await ctx.respond(rap + "\n*" + RptMsg + "*")
  except Exception as e:
     await ctx.respond("Oops!")
     print(e)

#Run discord bot
bot.run(token)