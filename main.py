import discord
import os
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
from checks import *

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
  print("logged in as {0.user}".format(bot))

@bot.event
async def on_member_join(member):
  if member.guild.id == 887731729660538950 and member.bot == False:
    dbKey = (str(member.guild.id) + "onJoinRole")
    numeric_filter = filter(str.isdigit, db[dbKey])
    numeric_string = "".join(numeric_filter)
    role = member.guild.get_role(int(numeric_string))
    await member.add_roles(role, reason="User \"" + member.name + "\" with id: " + str(member.id) + " Joined")

@bot.command()
async def set_join_role(ctx, input):
  if input == None:
    ctx.send("Please define a role! Syntax: !set_join_role <@role>")
  else:
    dbKey = (str(ctx.guild.id) + "onJoinRole")
    roleId = input
    db[dbKey] = str(roleId)
    await ctx.send("The default role has been set to: " + input)

@bot.command()
@commands.has_permissions(administrator=True)
async def join_role(ctx, arg=None, input=None):
  dbKey = (str(ctx.guild.id) + "onJoinRole")
  if arg == None or arg.lower() == "current":
    await ctx.send(db[dbKey])
  elif arg.lower() == "clear":
    db[dbKey] = None
    await ctx.send("Join role has been cleared!")
  elif arg.lower() == "set":
    if input == None:
      ctx.send("Please define a role! Syntax: !join_role set <@role>")
    else:
      dbKey = (str(ctx.guild.id) + "onJoinRole")
      roleId = input
      db[dbKey] = str(roleId)
      await ctx.send("The default role has been set to: " + input)
  else:
    ctx.send("error please use correct syntax!")

@bot.command()
async def test(ctx):
  await ctx.send("hello world!")

keep_alive()
bot.run(os.getenv("TOKEN"))