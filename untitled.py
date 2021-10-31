import colorama
import discord
import json
import traceback

from discord.ext import commands
from colorama import Fore

colorama.init()

msgs = {"info": f"{Fore.WHITE}[{Fore.CYAN}i{Fore.WHITE}]",
        "+": f"{Fore.WHITE}[{Fore.CYAN}+{Fore.WHITE}]",
        "-": f"{Fore.WHITE}[{Fore.CYAN}-{Fore.WHITE}]", 
        "error": f"{Fore.WHITE}[{Fore.RED}e{Fore.WHITE}]",
        "input": f"{Fore.WHITE}{Fore.CYAN}>>{Fore.WHITE}"}

async def msg_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        print(f"{msgs['error']}Can't delete your message")

print(f'{Fore.CYAN}\n\n                  __  __  __   __  ______ __  ______ __      ______  _____     ' + "\n"
                        r'                 /\ \/\ \/\ "-.\ \/\__  _/\ \/\__  _/\ \    /\  ___\/\  __-.  ' + "\n"
                        r'                 \ \ \_\ \ \ \-.  \/_/\ \\ \ \/_/\ \\ \ \___\ \  __\\ \ \/\ \ ' + "\n"
                        r'                  \ \_____\ \_\\"\_\ \ \_\\ \_\ \ \_\\ \_____\ \_____\ \____- ' + "\n"
                        r'                   \/_____/\/_/ \/_/  \/_/ \/_/  \/_/ \/_____/\/_____/\/____/ ' + "\n"
                        '\n'
                        r'                           __   __  __  __  __  __  ______  ______    ' + "\n"
                        r'                          /\ "-.\ \/\ \/\ \/\ \/ / /\  ___\/\  == \   ' + "\n"
                        r'                          \ \ \-.  \ \ \_\ \ \  _"-\ \  __\\ \  __<   ' + "\n"
                        r'                           \ \_\\"\_\ \_____\ \_\ \_\ \_____\ \_\ \_\ ' + "\n"
                        r'                            \/_/ \/_/\/_____/\/_/\/_/\/_____/\/_/ /_/ '
                        "\n"
                        "\n"
                        "\n"
                        f"{Fore.WHITE}                                        Author: {Fore.CYAN}ICE#4449\n"
                        f"{Fore.WHITE}                                        Version: {Fore.CYAN}1.0.0\n"
                        f"{Fore.WHITE}                                        GitHub: {Fore.CYAN}*Link*\n"
                        "\n"
                        f"                            {Fore.WHITE}{Fore.CYAN}!{Fore.WHITE} Use for educational purpose only {Fore.CYAN}!{Fore.WHITE}\n\n")

try:
    with open(f"config.json", encoding='utf8') as data:
        config = json.load(data)
    token = config["token"]
    prefix = config["prefix"]
    owners = config["owners"]
    print(f'{msgs["info"]} Loaded config.json"')
except FileNotFoundError:
    token = input(f"Paste token {msgs['input']} ")
    prefix = input(f"Paste prefix {msgs['input']} ")
    owners = input(f"Paste bot's owner ID (If several use ',') {msgs['input']} ")
    owners = owners.replace(" ", "")
    if "," in owners:
        owners = owners.split(",")
        owners = list(map(int, owners))
    config = {
        "token": token,
        "prefix": prefix,
        "owners": owners
    }
    with open("config.json", "w") as data:
        json.dump(config, data, indent=2)
    print(f"{msgs['info']}Created config.json")

bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"\n\n{Fore.CYAN}" + ("═"*75).center(95) + f"\n{Fore.WHITE}" + 
            f"Logged in as {bot.user}".center(95) + "\n" + 
            f"Prefix: {prefix}".center(95) + "\n" + 
            f"Total servers: {len(bot.guilds)}".center(95) + "\n" + 
            f"Total members: {len(bot.users)} ".center(95) + f"\n{Fore.CYAN}" + ("═"*75).center(95) + "\n\n")

@bot.event
async def on_command_error(ctx, err):
    errors = commands.errors
    if isinstance(err, errors.BadArgument):
        return
    elif isinstance(err, errors.CommandInvokeError):
        print(f"{msgs['error']} Missing permissions")
    else:
        print(f'{Fore.RED}\n\n{"".join(traceback.format_exception(type(err), err, err.__traceback__))}{Fore.WHITE}\n')

@bot.command(name='ab')
async def banAllMembers(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if str(m.id) not in owners:
            await m.kick()
            print(f"{msgs['+']} Banned {m.name}")
        else:
            print(f"{msgs['info']} {m.name} is owner")

@bot.command(name='ak')
async def kickAllMembers(ctx):
    await msg_delete(ctx)
    for m in ctx.guild.members:
        if m.id not in owners:
            await m.kick()
            print(f"{msgs['+']} Kicked {m.name}")
        else:
            print(f"{msgs['info']} {m.name} is owner")

bot.run(token)