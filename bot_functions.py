# companion file to help keep list_manager.py tidy
from sqlite3 import dbapi2
import mysql.connector
import json

#----------- dealign with web settings ---------------
# Ignore SSL certificate errors
from urllib.request import urlopen
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# helper function to keep code tidy
def get_db():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database = "watch_lichess"
    )
    return mydb

# returns list of players with status = True
def get_in_play():
    mydb = get_db()
    mycursor = mydb.cursor()
    mycursor.execute("select handle from watch_users where status = True;")
    players = []
    rstr =""
    for i in mycursor: players.append(i[0])
    if len(players) > 0:
        for x in players: rstr = rstr + ", " +  x
        rstr = "Plaing now on Lichess: " + rstr[2:]  
    else:
        rstr = "There is currently no one from the Watch Party List playing on Lichess"
    return rstr

# returns the full list of players in the watch party list (watch_users table)
def get_full_list():
    mydb = get_db()
    mycursor = mydb.cursor()
    mycursor.execute("select handle from watch_users;")
    players = ""
    for i in mycursor: players = players +", " + i[0]
    players = players[2:]
    return "Here is the current watch party roster: " + players

#checks to see if player is already on watch party list
def check_player(content):
    player = content.strip().split()[1]
    mydb = get_db()
    mycursor = mydb.cursor()
    reply = "No, user " + player +" is not currently on the watchlist"
    sql_str = "select count(*) from watch_users where handle = '" + player +"';" 
    mycursor.execute(sql_str)   
    for i in mycursor: 
        if i[0] == 1: reply = "Yes, user " + player +" is on the watchlist"
    return reply

# adds discord user to list of lichess players to follow
def follow_player(content, discord_id):
    inp = content.strip().split()
    if len(inp) > 1:
        lichess = inp[1]
        retr_str =""
        #janky way to leverage the check_player method :(
        if check_player("holder " + lichess).startswith("Y"):
            mydb = get_db()
            mycursor = mydb.cursor()
            sql_str = "select count(*) from followers where lichess_name = '" + lichess.strip() + "' and discord_id = '" + discord_id.strip() + "';"
            mycursor.execute(sql_str)
            for i in mycursor: 
                if i[0] == 0: 
                    insert_str = "insert into followers(lichess_name, discord_id) values ('" + lichess.strip() + "', '" + discord_id.strip() +"');"
                    mycursor = mydb.cursor()
                    mycursor.execute(insert_str)
                    mydb.commit()
                    retr_str = "You are now following " + lichess.strip()
                else:
                    retr_str = "You are already following " + lichess.strip()
        else:
            retr_str = lichess.strip() + " is not on the watch list" 
    else:
        retr_str = "Please let me know who you would like to follow"
    return retr_str
    

# adds discord user to list of lichess players to follow
def unfollow_player(content, discord_id):
    inp = content.split()
    if len(inp) > 1:
        lichess = inp[1]
        if check_player("holder " + lichess).startswith("Y"):
            retr_str ="Okay, More notifications for when " +lichess.strip() + " starts playing on Lichess"
            mydb = get_db()
            mycursor = mydb.cursor()
            sql_str = "delete from followers where lichess_name = '" +lichess.strip() + "' and discord_id = '" + discord_id.strip() +"';" 
            mycursor.execute(sql_str)
            mydb.commit()
        else:
            retr_str = lichess + " is not on the watch party list"
    else:
        retr_str = "Please let me know who you'd like to unfollow"
    return retr_str

#returns a list of lichess players discord user is currently following
def get_my_follows(discord_id):
    retr_str = ""
    mydb = get_db()
    mycursor = mydb.cursor()
    sql_str = "select lichess_name from followers where discord_id = '" + discord_id.strip() + "';"
    mycursor.execute(sql_str)
    follows = []
    for i in mycursor: follows.append(i[0])
    if len(follows) > 0:
        for x in follows: retr_str = retr_str + ", " + x
        retr_str = "You are following " + retr_str[2:]
    else:
        retr_str = "You are not following anyone"
    return retr_str

def add_player(lichess):
    retr_str = "something went wrong"
    mydb = get_db()
    mycursor = mydb.cursor()
    #check to see if user is in db
    sql_str = "select count(*) from watch_users where handle = '" + lichess.strip() + "';"
    x = None
    mycursor.execute(sql_str)
    for i in mycursor: 
        x = i[0]
    if x > 0:
        retr_str = lichess + " is already on the watch list"
    else:
        url = 'https://lichess.org/api/users/status?ids=' + lichess.strip()
        html = urlopen(url, context=ctx).read()
        stat = json.loads(html.decode('utf-8'))
        if len(stat)>0:
            mycursor = mydb.cursor()
            ist_str = "insert into watch_users(handle, status) values ('" + lichess.strip() + "', False);"
            mycursor.execute(ist_str)
            mydb.commit()
            retr_str = lichess + " is now part of the watch list."
        else:
            retr_str = lichess + " does not appear to be a Lichess Handle"
    return retr_str

def remove_player(lichess):
    retr_str = ""
    mydb = get_db()
    mycursor = mydb.cursor()
    #check to see if user is in db
    sql_str = "select count(*) from watch_users where handle = '" + lichess.strip() + "';"
    x = None
    mycursor.execute(sql_str)
    for i in mycursor: 
        x = i[0]
    if x > 0:
        mycursor = mydb.cursor()
        del_str = "delete from watch_users where handle = '" + lichess.strip() + "';"
        mycursor.execute(del_str)
        mydb.commit()
        retr_str = lichess + " has been removed the watch party list"
    else:
        retr_str = lichess + " is not currently part of the watch party list"
    return retr_str



# check_player("!lwpCheck fake_Switch") 

# follow_player("!lwpFollow fauxtog", "fake_switch")
# follow_player("!lwpFollow DrNykterstein", "fake_switch")
# get_my_follows("fauxtog")
# get_my_follows("fake_switch")
# unfollow_player("!lwpunFollow DrNyktersteiasdfasdfn", "fake_switch")
