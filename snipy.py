import asyncio
import urllib.parse
import discord
import os
import requests
import subprocess as sp
from colorama import init, Fore
from time import perf_counter
from discord.ext import commands

f = open("delay.txt", "r")
customdelay = int(f.readline())

def command_prefix(bot, message):
    if message.guild is None:
        return ''
    else:
        return '-'

waitingresponses = []
ign1 = ""
ctx1 = ""
output = "test"
client = commands.Bot(command_prefix = command_prefix)

@client.event
async def on_ready():
    print('Snipy is ready!')

@client.event
async def on_message(message):
    if message.guild is None:
        if message.author in waitingresponses:
            file = open("accounts.txt", "w")
            file.write(message.content)
            file.close()
            await setsnipe(ctx1, ign1)

    await client.process_commands(message)

@client.command(pass_context=True)

async def delay(ctx, delayamount):
    file = open("delay.txt", "w")
    file.write(delayamount)
    file.close()
    await ctx.send(f"{ctx.author.mention} Set the delay to {delayamount}")

@client.command(pass_context=True)

async def snipe(ctx, ign):
    global ctx1
    global ign1
    ctx1 = ctx
    ign1 = ign
    await ctx.send(f"{ctx.author.mention} Please check your DM!")
    await ctx.author.send("Please provide your details (Format: email:password:security_question1_answer:security_question2_answer:security_question3_answer):")
    waitingresponses.append(ctx.author)

async def setsnipe(ctx, ign):

        namemc_output = requests.get(f'https://namemc.com/name/{ign}')
        snipe_time = namemc_output.text.split('<time id="availability-time" class="text-nowrap" datetime="')[1].split('</time>')[0].replace('T', ' @ ').split('Z"')[0].replace('.000', ' UTC')

        embed = discord.Embed(
            title = 'New Snipe :boom:',
            description = 'A new snipe has been set. Good luck!',
            color=discord.Color.red()
        )
        embed.set_author(name=ctx.author.display_name, url="https://discordapp.com/users/283305964311150592", icon_url=ctx.author.avatar_url)
        embed.add_field(name="Ign", value=ign, inline=True)
        embed.add_field(name="Time", value=snipe_time, inline=True)

        delay = f"{await check('https://api.minecraftservices.com/minecraft')}"

        print('[SNIPY][LOG] {0.author.display_name} has requested an snipe for "{1}"'.format(ctx.message, ign))
        print(f"[SNIPY][IGN] Set to '{ign}'")
        print(f"[SNIPY][DELAY] Set to '{delay}'")

        await ctx.send(embed=embed)
        await gosnipe(ctx, ign, delay)

async def gosnipe(ctx, ign, delay):

        output = sp.getoutput(f"python snipy-snipe.py {ign} snipe {delay}")
        email = output.split('[success] signed in to ')[1].split('[info]')[0]
        emaildomain = email.split('@')[1]
        output = output.replace(email, f"*****{emaildomain}")
        embed = discord.Embed(
            title = 'Snipe Result :newspaper:',
            description = f'```{output}```',
            color=discord.Color.blue()
        )

        await ctx.send(embed=embed)


async def check(url: str):
    async def x():
        uri = urllib.parse.urlparse(url)
        reader, writer = await asyncio.open_connection(uri.hostname, 443, ssl=True)
        writer.write(f"GET {uri.path or '/'} HTTP/1.1\r\nHost:{uri.hostname}\r\n\r\n".encode())

        start = perf_counter()
        await writer.drain()

        await reader.read(1)
        end = perf_counter()
        return round((end - start) * 1000)

    pings = []

    for _ in range(5):
        pings.append(await x())
        await asyncio.sleep(0.01)
    print(customdelay)
    return f"{round(sum(pings)/5+customdelay)}"

client.run('YOUR-API-KEY')
