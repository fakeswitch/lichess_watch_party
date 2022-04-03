
import discord
from discord.ext import commands
import bot_functions as bf
import helper as h

#---------- import logging?-------
import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#logging.basicConfig(level=logging.INFO)
#intents = discord.Intents.default()
#intents.members = True

#bot = commands.Bot(command_prefix='?', description=description, intents=intents)
bot = commands.Bot(command_prefix='^')


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

#------------------------------general user functrions ----------- 

# get a list of commands this bot offers
@bot.command()
async def commands(ctx):
    retr_str = "^playing, ^list, ^mylist, ^check lichess_user_name, ^follow lichess_user_name, ^follow_all, ^unfollow lichess_user_name, ^unfollow_all, ^add lichess_user_name, ^remove lichess_user_name, ^openings lichess_user_name"
    await ctx.send(retr_str)

# who is currently playing
@bot.command()
async def playing(ctx):
    await ctx.send(bf.get_in_play())

# full list
@bot.command()
async def list(ctx):
    await ctx.send(bf.get_full_list())

# list user is currently following
@bot.command()
async def mylist(ctx):
    await ctx.send(bf.get_my_follows(str(ctx.author.mention)))

# particular person on this list
@bot.command()
async def check(ctx, lichess):
    await ctx.send(bf.check_player(ctx.message.content))


#-------------------follow/unfollow functions for discord ----------- 

# follow a licess user
@bot.command()
async def follow(ctx, lichess):
    await ctx.send(bf.follow_player(ctx.message.content, str(ctx.author.mention)))

# i've made a mistake and i want to follow anyone
@bot.command()
async def follow_all(ctx):
    retr_str = bf.follow_everyone(str(ctx.author.mention))
    await ctx.send(retr_str)

# list user is currently following
@bot.command()
async def unfollow(ctx, lichess):
    await ctx.send(bf.unfollow_player(ctx.message.content,str(ctx.author.mention)))

# i've made a mistake and no longer want to follow anyone
@bot.command()
async def unfollow_all(ctx):
    retr_str = bf.unfollow_everyone(str(ctx.author.mention))
    await ctx.send(retr_str)

#-------------------add/remove from watch list functions for mods ----------- 

# add lichess user to watch party master list
# restricted to people who have permission to ban members 
@bot.command()
async def add(ctx, lichess):
    retr_str = "Please ask a Mod to add people to the watchlist"
    if ctx.author.permissions_in(ctx.channel).ban_members:
        retr_str = bf.add_player(lichess)
    await ctx.send(retr_str)

# add lichess user to watch party master list
# restricted to people who have permission to ban members 
@bot.command()
async def remove(ctx, lichess):
    retr_str = "Please ask a Mod to remove people to the watchlist"
    if ctx.author.permissions_in(ctx.channel).ban_members:
        retr_str = bf.remove_player(lichess)
    await ctx.send(retr_str)

#---------------------- player stat commands   
# get top 3 opening moves of a player when they play white
@bot.command()
async def openings(ctx, *args):
    await ctx.send(bf.get_top_open(args))

# get ratings of bullet/blitz/rapid/classical/puzzles of a player
@bot.command()
async def ratings(ctx, user):
    await ctx.send(bf.get_cur_ratings(user))

#---------------------- silly commands
@bot.command()
async def haiku(ctx):
    await ctx.send(bf.make_haiku())

#------------------------- connect bot to discord-------------
bot.run(h.bat)