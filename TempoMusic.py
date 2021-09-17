import discord
from discord.ext import commands
import youtube_dl
import os

token = 'ODg4MDc2NTU1OTg3ODQ5MjI2.YUNbvg.gnSaNApx-MO_CkboAyFsE4qEJsk'

client = commands.Bot(command_prefix="!")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game('Beta version'))
    print(f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----")

@client.command()
async def stats(ctx):
    pythonVersion = platform.python_version()
    dpyVersion = discord.__version__
    serverCount = len(client.guilds)
    memberCount = len(set(client.get_all_members()))

    embed = discord.Embed(title=f'{client.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

    embed.add_field(name='Bot Version:', value=client.version)
    embed.add_field(name='Python Version:', value=pythonVersion)
    embed.add_field(name='Discord.Py Version', value=dpyVersion)
    embed.add_field(name='Total servers:', value=serverCount)
    embed.add_field(name='Total Users:', value=memberCount)
    embed.add_field(name='Bot Developers:', value="<@300210758757777408> <@262466223122546688>")

    embed.set_footer(text=f"Lnwdech, Kittipatzy | {client.user.name}")
    embed.set_author(name=client.user.name, icon_url=client.user.avatar_url)

    await ctx.send(embed=embed)

@client.command()
async def play(ctx, *url_raw):
    url = ""
    for i in url_raw:
        url = url + i + " "
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("Wait for the current playing music to end or use the 'stop' command")
        return
    voiceChannel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await ctx.send("อยู่ในห้องอยู่แล้ว")
    else:
        voice = await voiceChannel.connect()

    ydl_opts = {
        'default_search': 'ytsearch',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    await ctx.send(f'**Searching:** ' + url)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        info = ydl.extract_info(url, download=False)
        print(info)
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    if url.startswith("https://"):
        await ctx.send(f'**Now Playing:** ' + info["title"])
        await ctx.send(f'`Video URL:` '+info["webpage_url"])
    else:
        await ctx.send(f'**Now Playing:** ' + info["entries"][0]["title"])
        await ctx.send(f'`Video URL:` ' + info["entries"][0]["webpage_url"])


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("ยังไม่ได้เข้าห้อง")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.pause()
    else:
        await ctx.send("ไม่มีเพลงให้หยุด")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        voice.resume()
    else:
        await ctx.send("ไม่มีเพลงให้หยุด")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        voice.stop()
    else:
        await ctx.send("ยังไม่ได้เข้าห้อง")

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping = {round(client.latency * 1000)} ms')


client.run(token)
