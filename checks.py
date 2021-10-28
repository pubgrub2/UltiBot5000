import discord
import os
from discord.ext import commands

def admin_or_permissions(arg):
  async def arg1():
    return arg
  async def predicate(ctx):
    if ctx.autor.id == ctx.guild.owner_id:
      return True
    return ctx.guild is not None and ctx.author.guild_permissions.administrator or ctx.author.guild_permissions.arg1
  return commands.check(predicate)

def in_voice_channel():
  def predicate(ctx):
    return ctx.author.voice and ctx.author.voice.channel
  return commands.check(predicate)