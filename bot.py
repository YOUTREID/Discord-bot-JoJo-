import os
import time
import praw
import shutil
import random
import discord
import youtube_dl
from itertools import cycle
from discord.utils import get
from discord.ext import commands, tasks


client = commands.Bot(command_prefix = '.')
client.remove_command('help')

initial_role = 'Peasants'

reddit = praw.Reddit()


'''

rant space for john john


'''

# ----events----

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game('with my stand | .help | .music'))
    # change_status.start()
    print('Bot is ready')

@client.event
async def on_member_join(member):
    role = get(member.guild.roles, name = initial_role)
    await member.add_roles(role)
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')


# ----commands----

# ----reddit----
@client.command()
async def memes(ctx, subreddit_name = 'memes'):
    subreddit = reddit.subreddit(subreddit_name)

    posts = subreddit.hot(limit = 6)
    counter = 0
    for submission in posts:
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter == 3):
                break

@client.command()
async def jokes(ctx):
    subreddit = reddit.subreddit('jokes')
    counter = 0
    hot_memes = subreddit.hot(limit = 3)
    for submission in hot_memes:
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter == 3):
                break

@client.command(aliases = ['reddit'])
async def search(ctx, *, keyword):
    counter = 0
    for submission in reddit.subreddit('all').search(keyword):
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter == 3):
                break

@client.command(aliases = ['test'])
async def ping(ctx):
    await ctx.send('`Pong!`')

@client.command()
async def twice(ctx):
    subreddit = reddit.subreddit('twice')
    hot_memes = subreddit.hot(limit = 6)
    counter = 0
    for submission in hot_memes:
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter == 3):
                break

@client.command()
async def mina(ctx):
    subreddit = reddit.subreddit('MyouiMina')
    hot_memes = subreddit.hot(limit = 6)
    counter = 0
    for submission in hot_memes:
        if not submission.stickied:
            await ctx.send(submission.url)
            counter += 1
            if (counter == 3):
                break

#----general----

@client.command(aliases = ['pingfr'])
async def latency(ctx):
    await ctx.send(f'`{round(client.latency * 1000)}ms`')

@client.command()
async def clear(ctx, amount = 3):
    await ctx.channel.purge(limit = amount)

@client.command(aliases = ['clearall'])
async def nuke(ctx):
    await ctx.channel.purge(limit = 50)

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
    await ctx.send('Ora Ora Ora JoJo bot by John John Ora Ora Ora')

@client.command()
async def version(ctx):
    await ctx.send('Version 1.1.2')

@client.command(aliases = ['siri'])
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
Info and General:
.ping
.info
.version

Tools:
.nuke (use with caution, or don't)
.help
.clear
.music
.latency

Memes:
.siri
.mina
.twice
.memes
.jokes
.reddit
.oraoraora

NSFW:
#help```""")


# ----music commands----
@client.command()
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}')
    await ctx.send(f'Joined {channel}')

@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')
    else:
        await ctx.send('Yare Yare Daze. Currently not in a voice channel.')


@client.command(aliases = ['p'])
async def play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queued song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return

        else:
            queues.clear()
            print("No songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue" 
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue folder")

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.10

    try:
        await ctx.send(f"Playing: {name[:-16]}")
        print("playing\n")
    except:
        await ctx.send(f'Playing song')

@client.command()
async def pause(ctx):

    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Music paused")
        voice.pause()
        await ctx.send("Paused")
    else:
        print("Music not playing failed to pause")
        await ctx.send("Yare Yare Daze failed to pause")

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed")
    else:
        print("Music is not paused")
        await ctx.send("Yare Yare Daze music is not paused")

@client.command()
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    queues.clear()

    queue_infile = os.path.isdir('./Queue')
    if queue_infile is True:
        shutil.rmtree('./Queue')

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("Yare Yare Daze failed to stop")

queues = {}

@client.command(aliases = ['q'])
async def queue(ctx, url :str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num = len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl': queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    await ctx.send("Adding song " + str(q_num) + " to the queue")

    print("Song added to queue\n")

@client.command(pass_context=True, aliases=['n', 's', 'skip'])
async def next(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing Next Song")
        voice.stop()
    else:
        print("No music playing")
        await ctx.send("Yare Yare Daze no music playing rn")

@client.command(aliases = ['musiccoammand', 'musichelp', 'music'])
async def musiccommands(ctx):
    await ctx.send("""```css
Music Commands
.join
.leave
.play
.pause
.stop
.resume
.queue
.skip```""")

client.run()