print("Bot Writen By: KAJ7#0001")
# Imports
import asyncio
import config
import discord
import datetime
from discord.ext import commands
import os
import logging
import random
import traceback
import sys
import inspect
import psutil

logging.basicConfig(level = logging.INFO, format="Telescope [%(levelname)s] | %(message)s")

async def get_prefix(bot, message):
    li = ['tel ', 'TEL ', 'Tel ', 'TEl ', 'TeL ', 'tEl ', 'tEL ', 'teL ']
    return commands.when_mentioned_or(*li)(bot, message)

intents = discord.Intents.default()
#intents.members = True

# Set prefix and set case insensitive to true so the a command will work if miscapitlized
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True, intents=intents)

# Remove default help command
bot.remove_command("help")

@bot.command(aliases=['settings', 'h'])
async def help(ctx):
    await ctx.send(embed=discord.Embed(
        title="Telescope Commands",
        color=config.MAINCOLOR,
        description="Summarize anything with `tel summarize <content> <summary length (sentences)>`.\n\nYou can provide a link, text, message link, or a channel and message count to summarize. For example:\n`tel summarize https://en.wikipedia.org/wiki/Batman 3`\n`tel summarize https://discord.com/...3262 2`\n`tel summarize Lorem ipsum dolor sit amet...`\n`tel summarize #general 100 3`"
    ).add_field(
        name="Misc",
        value="`help`, `info`, `invite`",
        inline=False
    ).set_thumbnail(url=bot.user.avatar_url))

@bot.command(aliases = ['join'])
async def invite(ctx):
    await ctx.send(embed=discord.Embed(description="[**Invite Link**](https://discord.com/api/oauth2/authorize?client_id=818602531370041353&permissions=2147863616&redirect_uri=https%3A%2F%2Fdiscord.gg%2Fbread&scope=bot) 🔗", color = config.MAINCOLOR))

# Cogs
cogs = ["Eval", "Summarize", "StatCord"]

# Starts all cogs
for cog in cogs:
    bot.load_extension("Cogs." + cog)

# Check to see if the user invoking the command is in the OWNERIDS config
def owner(ctx):
    return int(ctx.author.id) in config.OWNERIDS

# @bot.check
# def check_for_blacklist(ctx):
#     if ctx.guild is not None:
#         server = config.get_server(ctx.guild.id)
#         return not ctx.channel.id in server['blacklist']
#     else:
#         return True

# Restarts and reloads all cogs
@bot.command()
@commands.check(owner)
async def restart(ctx):
    """
    Restart the bot.
    """
    restarting = discord.Embed(
        title = "Restarting...",
        color = config.MAINCOLOR
    )
    msg = await ctx.send(embed = restarting)
    for cog in cogs:
        bot.reload_extension("Cogs." + cog)
        restarting.add_field(name = f"{cog}", value = "✅ Restarted!")
        await msg.edit(embed = restarting)
    restarting.title = "Bot Restarted"
    await msg.edit(embed = restarting)
    logging.info(f"Bot has been restarted succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
    await msg.delete(delay = 3)
    if ctx.guild != None:
        await ctx.message.delete(delay = 3)

# Kills the bot
@bot.command()
@commands.check(owner)
async def kill(ctx):
    """
    kill the bot.
    """
    sys.exit(0)

@bot.event
async def on_guild_join(guild):
    logging.info("JOINED guild " + guild.name + " | current guilds: " + str(len(bot.guilds)))

@bot.event
async def on_guild_remove(guild):
    logging.info("LEFT guild " + guild.name + " | current guilds: " + str(len(bot.guilds)))

# Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    elif isinstance(error, commands.errors.CheckFailure):
        pass
    elif isinstance(error, commands.errors.UserInputError):
        pass
    elif isinstance(error, commands.errors.MemberNotFound):
        embed = discord.Embed(
            title = "User not found",
            #description = f"An error has occured while executing this command, please join the support server and report the issue!",
            color = config.ERRORCOLOR
        )
        await ctx.send(embed = embed)
    else:
        await ctx.send(content="An error has occured while executing this command.")
        raise error

# On ready
@bot.event
async def on_ready():
    logging.info(f"Bot has started succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users!")

    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name="pan help"))

@bot.command(aliases=['about'])
async def info(ctx):
    embed = discord.Embed(title="Telescope Bot Info", color=config.MAINCOLOR, timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=str(bot.user.avatar_url))

    embed.description = f"[Github Repo](https://github.com/kajdev/telescope)\n[Home Server](https://discord.gg/bread)"

    u = 0
    for g in bot.guilds:
        u+=g.member_count
    embed.add_field(name="Discord Stats", value=f"Guilds: `{len(bot.guilds)}`\nUsers: `{u}`\nAvg MSG/s: `{round(config.get_avg_messages(), 3)}`")

    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0]/2.**30  # memory use in GB...I think
    cpuUse = py.cpu_percent()
    embed.add_field(name="System Usage", value=f"Memory: `{round(memoryUse*1000, 3)} MB`\nCPU: `{round(cpuUse, 3)} %`")

    embed.set_footer(text=f"discord.py v{discord.__version__}")
    await ctx.send(embed=embed)

# Starts bot
bot.run(os.environ.get("TELESCOPE_TOKEN"))