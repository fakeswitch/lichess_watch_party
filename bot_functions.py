# companion file to help keep list_manager.py tidy
from sqlite3 import dbapi2
import mysql.connector
import json
import ndjson

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
        for x in players: rstr = rstr + ", " +  "https://lichess.org/@/{}/tv".format(x)
        rstr = "Playing now on Lichess: " + rstr[2:]  
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

# for people who want to follow eveyrone on the list... 
def follow_everyone(discord_id):
    mydb = get_db()
    mycursor = mydb.cursor()
    isrt_str = """
    insert into followers(lichess_name, discord_id)
    select handle, '{}' from watch_users where handle not in
    (select lichess_name from followers where discord_id = '{}');
    """
    mycursor.execute(isrt_str.format(discord_id, discord_id))
    mydb.commit()
    return "*sigh*... okay you are now following everyone on the current roster"
    
# remvoes the discord user/lichess_name pair from followers table 
def unfollow_player(content, discord_id):
    inp = content.split()
    if len(inp) > 1:
        lichess = inp[1]
        if check_player("holder " + lichess).startswith("Y"):
            retr_str ="Okay, No more notifications for when " +lichess.strip() + " starts playing on Lichess"
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

# removes every record from the followers table with the specified discord id
def unfollow_everyone(discord_id):
    mydb = get_db()
    mycursor = mydb.cursor()    
    del_str ="delete from followers where discord_id = '" + discord_id + "';"
    mycursor.execute(del_str)
    mydb.commit()
    retr_str = "You are no longer following anyone"
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

# adds lichess handle to watch_users table
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
        #check to see if id exists on lichess
        url = 'https://lichess.org/api/users/status?ids=' + lichess.strip()
        html = urlopen(url, context=ctx).read()
        stat = json.loads(html.decode('utf-8'))
        if len(stat)>0:
            # if lichess finds id, add to the watch_users table
            mycursor = mydb.cursor()
            ist_str = "insert into watch_users(handle, status) values ('" + lichess.strip() + "', False);"
            mycursor.execute(ist_str)
            mydb.commit()
            retr_str = lichess + " is now part of the watch list."
        else:
            #lichess did not find specified handle
            retr_str = lichess + " does not appear to be a Lichess Handle"
    return retr_str

# remove handle from watch_users table
def remove_player(lichess):
    retr_str = ""
    mydb = get_db()
    mycursor = mydb.cursor()
    #check to see if user is in db
    sql_str = "select count(*) from watch_users where handle = '" + lichess.strip() + "';"
    x = None
    mycursor.execute(sql_str)
    # check to see if handle is in table
    for i in mycursor: 
        x = i[0]
    if x > 0:
        # removes handle if exits
        mycursor = mydb.cursor()
        del_str = "delete from watch_users where handle = '" + lichess.strip() + "';"
        mycursor.execute(del_str)
        mydb.commit()
        retr_str = lichess + " has been removed the watch party list"
    else:
        # handle not found
        retr_str = lichess + " is not currently part of the watch party list"
    return retr_str

#--------- get user stat functions ---------

# get player top 3 openings as white
# expecting an list of at least one item (lichess user name), 
# optional second item for specific time controlls
def get_top_open(args_list):
    lichess = args_list[0]
    tc = "playing in all Time Controlls"
    if len(args_list) < 2:
        url = ' https://explorer.lichess.ovh/player?player={}&color=white'.format(lichess)
    else:
        url = ' https://explorer.lichess.ovh/player?player={}&color=white&speeds={}'.format(lichess,args_list[1])
        pretty_tc = args_list[1].replace(",", ", ")
        tc = "playing in {}".format(pretty_tc)
    html = urlopen(url, context=ctx).read()
    stat = ndjson.loads(html.decode('utf-8'))
    rg = 3
    if len(stat[0].get('moves')) < 3: 
        rg = len(stat[0].get('moves'))
    top3 ="Top {} openings (by times played) for {} {}:".format(rg, lichess, tc)
    for i in range(rg):
        move = stat[0].get('moves')[i].get('san')
        perform = stat[0].get('moves')[i].get('performance')
        white = stat[0].get('moves')[i].get('white')
        black =stat[0].get('moves')[i].get('black')
        draws = stat[0].get('moves')[i].get('draws')
        top3 += "\n1. {} with performace of {}, and record of +{} -{} ={}".format(move, perform, white, black, draws)
    return top3.strip()

# get current ratings
def get_cur_ratings(lichess):
    url = 'https://lichess.org/api/user/{}'.format(lichess)
    try:
        html = urlopen(url, context=ctx).read()
        user = json.loads(html.decode('utf-8'))
        tc = ['bullet', 'blitz', 'rapid', 'classical', 'puzzle']
        ret_string = "Current ratings for {}:".format(user.get('username'))
        for i in tc:
            j = user.get('perfs').get(i)
            rating = j.get('rating')
            rd = j.get('rd')
            games = j.get('games')
            ret_string += "\n{}: {} with a RD of {} in {} games".format(i.capitalize(), rating, rd, games)
    except: ret_string = 'Could not find user {}'.format(lichess)
    return ret_string.strip()


#---------- silly non chess related functions---------
def make_haiku():
    mydb = get_db()
    mycursor = mydb.cursor()
    mycursor.execute("use haiku;")
    #get random 5 sylb
    mycursor.execute("select * from rand_five limit 2;")
    hf = ""
    for l in mycursor: hf = hf + "," + str(l[0])
    hf = hf[1:]
    mycursor.execute("delete from rand_five where id in ({});".format(hf))
    mydb.commit()
    #get random 7 sylb
    mycursor.execute("select * from rand_seven limit 1;")
    hs = ""
    for m in mycursor: hs = str(m[0])
    mycursor.execute("delete from rand_seven where id in ({});".format(hs))
    mydb.commit()
    #get actual lines
    s = []
    l = []
    sql1 = "select id, verse from component where id in ({});".format(hf)
    sql2 = "select id, verse from component where id in ({});".format(hs)
    mycursor.execute(sql1)
    for i in mycursor: s.append((i[0],i[1]))
    mycursor.execute(sql2)
    for j in mycursor: l.append((j[0],j[1]))
    #store record of the created haiku
    sql3 = "insert into new_verses(l0_id,l1_id,l2_id) values ({},{},{})".format(s[0][0], l[0][0], s[1][0])
    mycursor.execute(sql3)
    mydb.commit()
    haiku = s[0][1].lower().capitalize() +"\n" +l[0][1].lower().capitalize() + "\n" + s[1][1].lower().capitalize()
    return haiku
