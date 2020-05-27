import discord
from discord.ext import commands, tasks

client = commands.Bot(command_prefix = '*')
client.remove_command('help')

trigger_symbols = ['!', '.', '>']

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game('Rythm'))
    # change_status.start()
    print('Bot is ready')

@client.event
async def on_message(message):
    if (message.author.name == "Rythm"):
        if (message.channel.name != 'music'):
            await message.delete()
    if (message.content[0] in trigger_symbols):
        if (message.channel.name != 'music'):
            await message.delete()
    

@client.command()
async def info(ctx):
    await ctx.send('This bot is made for those fuckers that use music commands in lobby.')



client.run('TOKEN')