# this script grabs a list of lichess usernames from a local database
# makes a request to the lichess api for the status of the users
# updates the user's status on the local db
# if there are any changes to the status (start or stop)
# will announce the change to discord through webhook
# script currently runs once every 3 minute

from urllib.request import urlopen
import ssl
import json
import mysql.connector
import helper
#import pandas as pd

#-----------discord settings ---------------
import requests
from discord import Webhook, RequestsWebhookAdapter
webhook = Webhook.from_url(helper.wh, adapter=RequestsWebhookAdapter())

#----------- dealign with web settings ---------------
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#----------- database settings settings ---------------
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "watch_lichess"
)
mycursor = mydb.cursor()

#---------------get new status of plays on watch list---------------
#set url of lichess api status
url = 'https://lichess.org/api/users/status?ids='

# read all users from users table into data stream
# limit 100 because that's the maximum allowed users to check on lichess at a time
sql_str = "SELECT * FROM watch_users limit 100;"
mycursor.execute(sql_str)

#adds users to list api url
for i in mycursor: url = url + i[0].strip() + ","

# ask lichess for status of users
html = urlopen(url, context=ctx).read()

#parse returned json
stat = json.loads(html.decode('utf-8'))

#manually add person playing for testing
# stat[0]["playing"] = 1

# create string that will help update values in bulk query
# sting in the format "('name', status)"
uds =""
for i in stat:
    statChg = "True"
    if i.get("playing",-1) == -1: 
        statChg = "False"
    uds = uds + "('" + i.get("id",-1) + "', " + statChg + "),"

# fixing fense post: get rid of the last "," in uds
uds = uds[:len(uds)-1]

# create temp table to hold the new status values
mycursor.execute("drop table if exists holder")
mycursor.execute("create temporary table holder (name varchar(255), status bool);")

# load new status values into temp table
mycursor.execute("insert into holder values " + uds + ";")

# get a temp table of users that changed
mycursor.execute("drop table if exists com_stat")
compare_table_str = """create temporary table com_stat
select h.* from watch_users u inner join holder h on h.name = u.handle where u.status <> h.status and h.status =1;"""
mycursor.execute(compare_table_str)

# update watch_users table with new values  
mycursor.execute("update watch_users u inner join holder h on u.handle = h.name set u.status = h.status")

# commit changes
mydb.commit()

# -------------- announce changes -----------
# make dictionary for status action
tv = "https://lichess.org/@/"
action = {}
action["1"] = "is now playing on Lichess".upper()
action["0"] = "has stopped playing"
shout = ""
# build string of that will be pushed to discord
# we axed the stopped playing prompt, but querying only games that have started in com_stat
mycursor.execute("select * from com_stat")
for i in mycursor: 
    shout = shout +i[0].upper() + " " + action[str(i[1])] 
    if str(i[1]) == "1" : shout = shout + " " + tv + i[0] + "/tv"
    shout = shout + ", "

# fixing fense post
shout = shout[:len(shout)-2]

# get list of users who wants to be notified
dis_id = "select distinct f.discord_id from com_stat c inner join followers f on c.name = f.lichess_name"
mycursor.execute(dis_id)
for y in mycursor: shout = shout + " " + y[0]



if len(shout)>1: webhook.send(shout)