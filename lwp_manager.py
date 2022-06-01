
import discord
from discord.ext import commands
import bot_functions as bf
import helper as h
import asyncio

#---------- import logging?-------
import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#bot = commands.Bot(command_prefix='?', description=description, intents=intents)
bot = commands.Bot(command_prefix='^')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#------------------------------general user functrions ----------- 
"""
# apparently there is a built in function from discord.ext called "help" that takes care of this
# i do need to figure out how to organize the commands though

# get a list of commands this bot offers
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def lc_commands(ctx):
    retr_str = "^playing, ^list, ^mylist, ^check lichess_user_name, ^follow lichess_user_name, ^follow_all, ^unfollow lichess_user_name, ^unfollow_all, ^add lichess_user_name, ^remove lichess_user_name, ^ratings lichess_user_name, ^openings lichess_user_name, ^response lichess_user_name first_move, ^openings2 lichess_user_name color move(s) time_controll"
    await ctx.send(retr_str)

@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def silly_commands(ctx):
    retr_str = "^haiku, ^dice sides_on_die number_of rolls, ^coin, ^m8 yes_no_question, ^joke, ^aww, ^trivia, ^anime, ^horo astro_sign, ^song"
    await ctx.send(retr_str)
"""

# who is currently playing
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def playing(ctx):
    await ctx.send(bf.get_in_play())

# full list
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def list(ctx):
    await ctx.send(bf.get_full_list())

# list user is currently following
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def mylist(ctx):
    await ctx.send(bf.get_my_follows(str(ctx.author.mention)))

# particular person on this list
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def check(ctx, lichess):
    await ctx.send(bf.check_player(ctx.message.content))


#-------------------follow/unfollow functions for discord ----------- 

# follow a licess user
# get a ping when specified player stars a game
@bot.command()
@commands.cooldown(1,10, commands.BucketType.user)
async def follow(ctx, lichess):
    await ctx.send(bf.follow_player(ctx.message.content, str(ctx.author.mention)))

# i've made a mistake and i want to follow anyone
# get a ping when anyone on the watch list starts a game
@bot.command()
@commands.cooldown(1,300, commands.BucketType.user)
async def follow_all(ctx):
    retr_str = bf.follow_everyone(str(ctx.author.mention))
    await ctx.send(retr_str)

# stop getting notifications for specific player
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def unfollow(ctx, lichess):
    await ctx.send(bf.unfollow_player(ctx.message.content,str(ctx.author.mention)))

# i've made a mistake and no longer want to follow anyone
@bot.command()
@commands.cooldown(1,30, commands.BucketType.user)
async def unfollow_all(ctx):
    retr_str = bf.unfollow_everyone(str(ctx.author.mention))
    await ctx.send(retr_str)

#-------------------add/remove from watch list functions for mods ----------- 

# add lichess user to watch party master list
# restricted to people who have permission to ban members 
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def add(ctx, lichess):
    retr_str = "Please ask a Mod to add people to the watchlist"
    if ctx.author.permissions_in(ctx.channel).ban_members:
        retr_str = bf.add_player(lichess)
    await ctx.send(retr_str)

# add lichess user to watch party master list
# restricted to people who have permission to ban members 
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def remove(ctx, lichess):
    retr_str = "Please ask a Mod to remove people to the watchlist"
    if ctx.author.permissions_in(ctx.channel).ban_members:
        retr_str = bf.remove_player(lichess)
    await ctx.send(retr_str)

#---------------------- player stat commands   
# get top 3 opening moves of a player when they play white
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def openings(ctx, *args):
    await ctx.send(bf.get_top_open(args))

# get top 3 responses moves of a player when they play black
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def response(ctx, *args):
    await ctx.send(bf.get_top_open_black(args))

# rebuilt openings function, combines the functions openings and response
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def opening2(ctx, lichess, color, moves, speeds):
    await ctx.send(bf.get_openings(lichess, color, moves, speeds))


# get ratings of bullet/blitz/rapid/classical/puzzles of a player
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def ratings(ctx, user):
    await ctx.send(bf.get_cur_ratings(user))

#---------------------- silly commands
# returns a haiku
@bot.command()
@commands.cooldown(1,15, commands.BucketType.guild)
async def haiku(ctx):
    await ctx.send(bf.make_haiku())

# rolls dice of specified sides and specified times
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def dice(ctx, sides, num):
    await ctx.send(bf.roll_dice(int(sides), int(num)))

# returns heads or tails
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def coin(ctx):
    await ctx.send(bf.coin())

# magic 8ball!
@bot.command()
@commands.cooldown(1,15, commands.BucketType.user)
async def m8(ctx, question):
    await ctx.send(bf.eightball())

# get a joke from reddit /r/cleanjokes and /r/dadjokes
@bot.command()
@commands.cooldown(1,17, commands.BucketType.guild)
async def joke(ctx):
    holder = bf.get_joke()
    await ctx.send(holder[0])
    await asyncio.sleep(12)
    await ctx.send(holder[1])
    
# fetch jpg url from animal subreddits
@bot.command()
@commands.cooldown(1,15, commands.BucketType.guild)
async def aww(ctx):
    await ctx.send(bf.reddit_aww())

# specifically, fetch a hamster jpg from flickr
@bot.command()
@commands.cooldown(1,15, commands.BucketType.guild)
async def hamster(ctx):
    await ctx.send(bf.get_flickr('cute hamster'))

# fetch a jpg from flickr
@bot.command()
@commands.cooldown(1,10, commands.BucketType.guild)
async def photo(ctx, kw):
    holder = "Here's a picture of {}:\n".format(kw)
    await ctx.send(holder + bf.get_flickr(kw))

# get a trivia from opentdb.com
@bot.command()
@commands.cooldown(1,25, commands.BucketType.guild)
async def trivia(ctx):
    holder = bf.get_trivia(0)
    await ctx.send(holder[0])
    await asyncio.sleep(20)
    await ctx.send(holder[1])

# get anime trivia from opentdb.com
@bot.command()
@commands.cooldown(1,25, commands.BucketType.guild)
async def anime(ctx):
    holder = bf.get_trivia(31)
    await ctx.send(holder[0])
    await asyncio.sleep(20)
    await ctx.send(holder[1])

# get random song recommendation from reddit
@bot.command()
@commands.cooldown(1,60, commands.BucketType.guild)
async def song(ctx):
    await ctx.send(bf.ask_reddit_song())

# give a horoscope!
@bot.command()
@commands.cooldown(1,60, commands.BucketType.user)
async def horo(ctx, sign):
    await ctx.send(bf.get_horoscope(sign))

#------------------------- connect bot to discord-------------
bot.run(h.bat)