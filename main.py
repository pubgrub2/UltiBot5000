import discord
import os
import time
#import nacl
from discord.ext import commands
from replit import db
from keep_alive import keep_alive
from checks import *
from discord import app_commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.message_content = True
activity = discord.Activity(type=discord.ActivityType.watching, name="you from the corner.")

bot = commands.Bot(command_prefix="!", intents=intents, activity=activity, status=discord.Status.online)

@bot.event
async def on_ready():
  print("logged in as {0.user}".format(bot)) # prints bot username and tag
  for x in bot.guilds:
    dbKeySaveKeys = ("save" + str(x.id) + "saveKeys")
    if dbKeySaveKeys not in db.keys():
      db[dbKeySaveKeys] = False
      print(str(x) + " with id: " + str(x.id) + " save keys was reset to false")

@bot.event
async def on_member_join(member):
  if member.bot == False:
    dbKeyJoinRole = (str(member.guild.id) + "onJoinRole")
    if dbKeyJoinRole in db.keys():
      numeric_filter = filter(str.isdigit, db[dbKeyJoinRole])
      numeric_string = "".join(numeric_filter)
      role = member.guild.get_role(int(numeric_string))
      await member.add_roles(role, reason="User \"" + member.name + "\" with id: " + str(member.id) + " Joined")

@bot.event
async def on_guild_join(guild):
  dbKeySaveKeys = ("save" + str(guild.id) + "saveKeys")
  if dbKeySaveKeys not in db.keys():
    db[dbKeySaveKeys] = False

@bot.event
async def on_guild_remove(guild):
  dbKeySaveKeys = ("save" + str(guild.id) + "saveKeys")
  if db[dbKeySaveKeys] != True:
    dbKeyGuildOccurances = db.prefix(guild.id)
    for x in dbKeyGuildOccurances:
      print(x)
      del db[x]

@bot.command()
@commands.has_permissions(administrator=True)
async def join_role(ctx, arg=None, input=None):
  dbKeyJoinRole = (str(ctx.guild.id) + "onJoinRole")
  if arg == None or arg.lower() == "current":
    if dbKeyJoinRole not in db.keys():
      await ctx.send("Currently there is no join role set, to set one, use the command \"!join_role set <@role>\".")
    else:
      await ctx.send("The current join role is: " + db[dbKeyJoinRole])
  elif arg.lower() == "clear":
    del db[dbKeyJoinRole]
    await ctx.send("Join role has been cleared!")
  elif arg.lower() == "set":
    if input == None:
      ctx.send("Please define a role. Syntax: \"!join_role set <@role>\".")
    else:
      dbKeyJoinRole = (str(ctx.guild.id) + "onJoinRole")
      roleId = input
      db[dbKeyJoinRole] = str(roleId)
      await ctx.send("The default role has been set to: " + input)
  else:
    ctx.send("error please use correct syntax!")

@bot.command()
@commands.has_permissions(administrator=True)
async def save_keys(ctx, arg=None):
  dbKeySaveKeys = ("save" + str(ctx.guild.id) + "saveKeys")
  if arg.lower() == "on":
    db[dbKeySaveKeys] = True
    await ctx.send("Settings are now being saved!")
  elif arg.lower() == "off":
    db[dbKeySaveKeys] = False
    await ctx.send("Settings are not being saved!")
  else:
    await ctx.send("Please use correct syntax: \"!save_keys on/off\".")

@bot.command(pass_context=True)
async def fard(ctx):
  voice_state = ctx.author.voice
  kaiHere = False
  if voice_state is not None:
    for x in voice_state.channel.members:
      kaiHere = False
      if x.id == 387673770824957954:
        kaiHere = True
        await ctx.send("BAN!")
        break
  if voice_state is not None and kaiHere == False:
    channel = ctx.author.voice.channel
    vc = await channel.connect()
    vc.play(discord.FFmpegPCMAudio("Audio/fard.mp3"))
    time.sleep(2)
    await ctx.voice_client.disconnect()
  elif kaiHere == False:
    await ctx.send("Please join a voice channel!")

@in_voice_channel()
@bot.command()
async def move(ctx, channel : discord.VoiceChannel):
  try:
    for members in ctx.author.voice.channel.members:
      await members.move_to(channel)
  except:
    await ctx.send("error")

@bot.hybrid_command(name = "test", description = "Tests the bot.")
async def test(ctx):
  await ctx.send("hello world!")

@bot.command()
async def reset_all_global_settings(ctx):
  if ctx.author.id == 347809578957930501:
    keys = db.keys()
    for x in keys:
      del db[x]
      await ctx.send(x + " has been deleted!")
    await ctx.send("done.")
  else:
    await ctx.send("ARE YOU TRYING TO PLAY BOT DEVELOPER?")

@bot.command()
async def list_key_values(ctx):
  if ctx.author.id == 347809578957930501:
    keys = db.keys()
    for x in keys:
      await ctx.send(str(x) + " " + str(db[x]))
    await ctx.send("done.")
  else:
    await ctx.send("are you trying to play bot developer?")

@bot.hybrid_command(name = "sync_commands", description = "Synchronizes application slash commands")
async def sync_commands(ctx):
  await bot.tree.sync()
  await ctx.send("Slash commands have been synchonized.")

keep_alive()
bot.run(os.getenv("TOKEN"))