import discord
import random
import time
import praw
from discord.ext import commands, tasks
from itertools import cycle

client = commands.Bot(command_prefix = '.')
client.remove_command('help')

# details taken away for privacy purposes
reddit = praw.Reddit()

status = cycle(['with my stand', '.help', '.memes', '.reddit', '.oraoraora'])

'''

rant space for john john


'''

# ----events----

@client.event
async def on_ready():
    #await client.change_presence(status = discord.Status.online, activity = discord.Game('with my stand | .help'))
    change_status.start()
    print('Bot is ready')

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@tasks.loop(seconds=60)
async def change_status():
    await client.change_presence(status = discord.Status.online, activity = discord.Game(next(status)))


# ----commands----

@client.command()
async def memes(ctx, subreddit_name = 'memes'):
    subreddit = reddit.subreddit(subreddit_name)

    hot_memes = subreddit.hot(limit = 5)
    for submission in hot_memes:
        if not submission.stickied:
            await ctx.send(submission.url)


@client.command()
async def jokes(ctx):
    subreddit = reddit.subreddit('jokes')

    hot_memes = subreddit.hot(limit = 3)
    for submission in hot_memes:
        if not submission.stickied:
            await ctx.send(submission.url)

@client.command(aliases = ['reddit'])
async def search(ctx, *, keyword):
    counter = 0
    for submission in reddit.subreddit('all').search(keyword):
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter != 3):
                continue
            break

@client.command()
async def ping(ctx):
    await ctx.send('`Pong!`')

@client.command(aliases = ['pingfr'])
async def latency(ctx):
    await ctx.send(f'`{round(client.latency * 1000)}ms`')

@client.command()
async def clear(ctx, amount = 5):
    await ctx.channel.purge(limit = amount)

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason = reason)
    await ctx.send(f'{member} has been kicked from the server.')

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    await ctx.send(f'{member} has been banned from the server.')

@client.command(aliases = ['oraoraora', 'oraora'])
async def ora(ctx):
    responses = ['https://gfycat.com/deadathleticdikdik',
                'https://imgur.com/gallery/1wb4XCj',
                ]
    await ctx.send(random.choice(responses))

@client.command()
async def info(ctx):
    await ctx.send('Ora Ora Ora I am a bot made by John John Ora Ora Ora')

@client.command()
async def version(ctx):
    await ctx.send('Version 1.0.5')

@client.command()
async def hentai(ctx):
    responses = ['https://hanime.tv/',
                'https://animeidhentai.com/',
                'https://hentaihaven.org/',
                'Just google it 4head']
    await ctx.send(f'Try this: {random.choice(responses)}')

@client.command(aliases = ['siri', 'hey_siri', 'ama'])
async def genie(ctx, *, question):
    responses = ['As I see it, yes.', 
                'Ask again later.',
                'Better not tell you now.',
                'Cannot predict now.',
                'Concentrate and ask again.',
                'Don’t count on it.',
                'It is certain.',
                'It is decidedly so.',
                'Most likely.',
                'My reply is no.',
                'My sources say no.',
                'Outlook not so good.',
                'Outlook good.',
                'Reply hazy, try again.',
                'Signs point to yes.',
                'Very doubtful.',
                'Without a doubt.',
                'Yes.',
                'Yes – definitely.',
                'You may rely on it.']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command(aliases = ['command', 'commands'])
async def help(ctx):
    await ctx.send("""```css
Commands
.help
.info
.ping
.siri
.clear
.memes
.jokes
.reddit
.hentai
.latency
.version
.oraoraora```""")

client.run()
