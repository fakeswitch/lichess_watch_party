
import discord
from discord.ext import commands
import bot_functions as bf
import helper as h

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

# follow a licess user
@bot.command()
async def follow(ctx, lichess):
    await ctx.send(bf.follow_player(ctx.message.content, str(ctx.author.mention)))

# list user is currently following
@bot.command()
async def unfollow(ctx, lichess):
    await ctx.send(bf.unfollow_player(ctx.message.content,str(ctx.author.mention)))

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

@bot.command()
async def commands(ctx):
    retr_str = "^playing, ^list, ^mylist, ^check, ^follow lichess_user_name, ^unfollow lichess_user_name, ^add lichess_user_name, ^remove lichess_user_name"
    await ctx.send(retr_str)
bot.run(h.bat)