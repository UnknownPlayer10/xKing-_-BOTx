#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import discord
import random
from discord.ext import commands
import logging
import traceback
import asyncio
import os
from discord import opus
from asyncio import sleep


logging.basicConfig(level='INFO')
bot = commands.Bot(command_prefix='k!½')
bot.remove_command('help')
bot.load_extension("music")
bot.load_extension("admin")
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

def load_opus_lib(opus_libs=OPUS_LIBS):
    if opus.is_loaded():
        return True
    for opus_lib in opus_libs:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass
    raise RuntimeError('Could not load an opus lib. Tried %s' % (', '.join(opus_libs)))
load_opus_lib()
    
@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command(name='8ball')
async def l8ball(ctx):
    await ctx.send(random.choice(['● It is certain.', '● It is decidedly so.', '● Without a doubt.', '● Yes - definitely.', '● You may rely on it', '● As I see it, yes.', '● Most likely.', '● Outlook good.', '● Yes.', '● Signs point to yes.', '● Reply hazy, try again', '● Ask again later.', '● Better not tell you now.', '● Cannot predict now.', '● Concentrate and ask again.', '● Don`t count on it.', '● My reply is no.', '● My sources say no', '● Outlook not so good.', '● Very doubtful.' ]))

    
@commands.cooldown(1, 5, commands.BucketType.user) 
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Please provide a user to kick")
    if member != ctx.author:
        await member.send(f'You just got kicked by **{ctx.message.author}** on ** {ctx.guild.name}** for **{reason}**')
        await member.kick()
        await ctx.send(f':white_check_mark: | **{member}** just got kicked.')

@bot.listen()
async def on_member_join(member):
    if member.guild.id == 461953532019605504:      
        e = discord.Embed(color=discord.Colour.blue())
        e.add_field(name=':hugging: Welcome!', value=member.mention, inline=False)
        e.add_field(name=':tools: Info:', value=f'**Bine ai venit pe {member.guild.name}! Nu uita sa citesti <#461959981936148511>. Speram sa te distrezi alaturi de noi! Acum suntem {member.guild.member_count}**', inline=False)
        e.set_thumbnail(url=member.avatar_url)
        await bot.get_guild(461953532019605504).get_channel(470916620332695562).send(embed=e)
    if member.guild.id != 461953532019605504:
        return





@bot.listen()
async def on_member_remove(member):
    if member.guild.id == 461953532019605504:      
        e = discord.Embed(color=discord.Colour.blue())
        e.add_field(name=':sob: Goodbye!', value=member.mention, inline=False)
        e.add_field(name=':tools: Info:', value=f'Speram sa te mai intorci pe la noi ... Esti mereu bine venit ! Acum Suntem {member.guild.member_count} :sob: :pensive:', inline=False)
        e.set_thumbnail(url=member.avatar_url)
        await bot.get_guild(461953532019605504).get_channel(470916620332695562).send(embed=e)
    if member.guild.id != 461953532019605504:
        return

@bot.check
async def botcheck(ctx):
    return not ctx.message.author.bot

@commands.cooldown(1, 5, commands.BucketType.user)     
@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member = None, *, reason = None):
    if member is None:
        await ctx.send(":x: | Please provide a user to ban")
    if member != ctx.author and member != ctx.bot.user:
        await member.send(f'You just got banned by **{ctx.message.author}** on ** {ctx.guild.name}** for **{reason}** ')
        await member.ban()
        await ctx.send(f':white_check_mark: | **{member}** just got banned.')
      
        
@bot.listen()
async def on_ready():
          print('Logging in as', bot.user.name)
       

@bot.command(aliases= ["clear", "prune", "delete"])
@commands.has_permissions(manage_channels=True)
async def purge(ctx, number : int):
    await ctx.message.delete()
    await ctx.channel.purge(limit=number)
    await ctx.message.channel.send(':thumbsup: | Messages deleted succefully!', delete_after=10)            
         
            

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def help(ctx):
    await ctx.send("""   ***xKing-_-BOTx Commands:***
**k!say** : Make the bot say whatever you want
**k!ping** : Check the bot latency
**k!search** : Search something on Google
**k!avatar** : Get a player's avatar
**k!8ball** : Ask the Magic 8-Ball)
**k!playerinfo @<member>** : Get a member`s info
**k!serverinfo** Get a guild/server info
**k!botinfo** : Get the bot info
**k!lenny** : Just a lenny face
**k!respect** : Pay #respect)
**k!kick** : Kick a member (works only if the player has the Kick perm.)
**k!ban** : Ban a member (works only if the player has the Ban perm.)
**k!mass** : Sends a message to all members in a guild (BOT Owner only)
**k!shutdown** : Shuts down the bot (BOT Owner only)
**k!purge** : Clears a number of messages (works only if the player has the Manage Channels perm.)
""")


@bot.listen()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        return await ctx.send(f':no_entry: | Hey, You are being ratelimited! Try again in** {int(error.retry_after)} **seconds!', delete_after=5)
    if isinstance(error, commands.CommandNotFound):
        return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
    error = error.__cause__ or error
    tb = traceback.format_exception(type(error), error, error.__traceback__, limit=2, chain=False)
    tb = ''.join(tb)
    fmt = 'Error in command {}\n\n{}:\n\n{}\n'.format(ctx.command, type(error).__name__, tb)
    print(fmt)

@bot.command()
async def support(ctx):
      await ctx.send('https://discord.gg/Xk6PDXu')


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def search(ctx, *, query):
    search = query
    URL = "https://www.google.com/search?q="
    words = search.split(" ")

    num = 0
    for w in words:
        if num is 0:
            URL = URL + w
            num = 1
        else:
            URL = URL + "+"+ w

    await ctx.send(URL)

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def say(ctx, *, message):
    """Make the BOT say what you want"""
    await ctx.send(f' {message}')

@commands.is_owner()
@bot.command()
async def mass(ctx, *, message):
    async def maybe_send(member):
        try:
            await member.send(message)
        finally:
            await ctx.message.delete()

    await asyncio.gather(*[maybe_send(m) for m in ctx.guild.members])


@commands.is_owner()
@bot.command()
async def shutdown(ctx):
    await ctx.send('Shutting down...')
    await sleep(5)
    await ctx.bot.logout()
   


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def ping(ctx):
    """Get your MS"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.green())
    em.set_author(name="")
    em.add_field(name="Ping", value='Pong! :ping_pong:', inline=True)
    em.add_field(name="MS", value=f'Took : **{ctx.bot.latency * 1000:,.2f}ms**', inline=True)
    await ctx.send(embed=em)


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def avatar(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title="", color=discord.Colour.blue())
    em.set_author(name=f"{member}'s avatar")
    em.set_image(url=member.avatar_url)
    msg = await ctx.send(embed=em)









@bot.command()
async def invite(ctx):
    em = discord.Embed(title="", color=discord.Colour.blue())
    em.add_field(name="Invite ***xKing-_-BOTx***", value='[Invite]( https://discordapp.com/api/oauth2/authorize?client_id=573128589273464832&permissions=8&scope=bot )')
    await ctx.send(embed=em)

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def lenny(ctx):
    """Get the lenny face"""
    await ctx.send("( ͡° ͜ʖ ͡° )")

@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def sinfo(ctx, member: discord.Member=None):
    """Get the server info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{ctx.guild.name}'s info", color=discord.Colour.blue())
    em.set_author(name="Server Info")
    em.add_field(name="Name", value=ctx.guild.name)
    em.add_field(name="ID", value=ctx.guild.id)
    em.add_field(name="Owner", value=ctx.guild.owner)
    em.add_field(name="Owner ID", value=ctx.guild.owner.id)
    em.add_field(name="Roles", value=len(ctx.guild.roles))
    em.add_field(name="Members", value=ctx.guild.member_count)
    em.add_field(name="Created", value=ctx.guild.created_at)
    em.set_thumbnail(url=ctx.guild.icon_url)
    msg = await ctx.send(embed=em)



@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def serverinfo(ctx, member: discord.Member=None):
    """Get the server info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{ctx.guild.name}'s info", color=discord.Colour.blue())
    em.set_author(name="Server Info")
    em.add_field(name="Name", value=ctx.guild.name)
    em.add_field(name="ID", value=ctx.guild.id)
    em.add_field(name="Owner", value=ctx.guild.owner)
    em.add_field(name="Owner ID", value=ctx.guild.owner.id)
    em.add_field(name="Roles", value=len(ctx.guild.roles))
    em.add_field(name="Members", value=ctx.guild.member_count)
    em.add_field(name="Created", value=ctx.guild.created_at)
    em.set_thumbnail(url=ctx.guild.icon_url)
    msg = await ctx.send(embed=em)



@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def respect(ctx):
    """Pay respect"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.green())
    em.set_author(name="")
    em.add_field(name=f"{ctx.author.name}", value='Press :regional_indicator_f: to pay respect', inline=True)
    msg = await ctx.send(embed=em)
    await msg.add_reaction('\N{regional indicator symbol letter f}')


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def playerinfo(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{member}'s info", color=discord.Colour.blue())
    em.set_author(name="Player info")
    em.add_field(name="Name", value=member.name)
    em.add_field(name="ID", value=member.id)
    em.add_field(name="BOT:", value=member.bot)
    em.add_field(name="Tag", value=member.discriminator)
    em.add_field(name="Top Role", value=member.top_role)
    em.add_field(name="Nick", value=member.nick)
    em.add_field(name="Joined", value=member.joined_at)
    em.set_thumbnail(url=member.avatar_url)
    msg = await ctx.send(embed=em)


@commands.cooldown(1, 5, commands.BucketType.user)
@bot.command()
async def pinfo(ctx, member: discord.Member=None):
    """Get your info"""
    if member is None:
        member = ctx.author
    em = discord.Embed(title=f"{member}'s info", color=discord.Colour.blue())
    em.set_author(name="Player info")
    em.add_field(name="Name", value=member.name)
    em.add_field(name="ID", value=member.id)
    em.add_field(name="BOT:", value=member.bot)
    em.add_field(name="Tag", value=member.discriminator)
    em.add_field(name="Top Role", value=member.top_role)
    em.add_field(name="Nick", value=member.nick)
    em.add_field(name="Joined", value=member.joined_at)
    em.set_thumbnail(url=member.avatar_url)
    msg = await ctx.send(embed=em)


async def presence():
    await bot.wait_until_ready()
    while not bot.is_closed():
        a = 0
        for i in bot.guilds:
            for u in i.members:
                if u.bot == False:
                    a = a + 1

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='%s users | k!help' % (len(bot.users))))
        await sleep(30)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='%s servers | k!help' % (len(bot.guilds))))
        await sleep(30)



@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def botinfo(ctx):
    """Get the BOT info"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="BOT Info")
    em.add_field(name="Name", value=ctx.bot.user.name, inline=True)
    em.add_field(name="ID", value=ctx.bot.user.id, inline=True)
    em.add_field(name="Prefix", value=ctx.bot.command_prefix, inline=True)
    em.add_field(name="Made with", value='Python 3.6.5', inline=True)
    em.add_field(name="Tag:", value=ctx.me.discriminator, inline=True)
    em.add_field(name="Creator", value='<@569808388297326593>', inline=True)
    em.add_field(name="Created at", value=ctx.bot.user.created_at, inline=True)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)
    




@commands.cooldown(1, 5, commands.BucketType.user)  
@bot.command()
async def binfo(ctx):
    """Get the BOT info"""
    em = discord.Embed(title="".format(ctx.guild.name), description="", color=discord.Colour.blue())
    em.set_author(name="BOT Info")
    em.add_field(name="Name", value=ctx.bot.user.name, inline=True)
    em.add_field(name="ID", value=ctx.bot.user.id, inline=True)
    em.add_field(name="Prefix", value=ctx.bot.command_prefix, inline=True)
    em.add_field(name="Made with", value='Python 3.6.5', inline=True)
    em.add_field(name="Tag:", value=ctx.me.discriminator, inline=True)
    em.add_field(name="Creator", value='<@569808388297326593>', inline=True)
    em.add_field(name="Created at", value=ctx.bot.user.created_at, inline=True)
    em.set_thumbnail(url=ctx.me.avatar_url)
    msg = await ctx.send(embed=em)
        






bot.loop.create_task(presence())
bot.run(os.getenv("TOKEN"))
