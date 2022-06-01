# watch party emcee
Encourage community engagement by keeping an eye out on who's currently playing games on lichess
There is currently no notification system in lichess that lets people know when their friends are online and playing
The intended use of this tool is to notify members of Discord Chess communities when fellow members are playing on lichess, so 
they can view games in real time and cheer them on in the lichess spectator rooms

This bot requires a mysql db called watch_lichess with a table called watch_users
The table should have two columns: handle(varchar) and status(bool)

emcee.py grabs all users from the table watch_users, than asks lichess about their current status, and updates table
this db does not keep history, just current status

If there is a change in status of a player to be actively in a live game, the script will announce to a dedicated Discord channel 
via webhook that the player is now playing and provides a link to the game.  This script does not announce when games have concluded

emcee.py is intended to be run by a scheduler. i recommend running the script every 3 minutes; seems to filter out most people
who want to play only 1 bullet game.

There is an accompanying script called lwp_manager.py that helps manage the watch party list.  
Mods of the Discord server can add and remove lichess usernames to the list
All members of the Discord server can use this tool to request to be pinged in the dedicated channel when specific players are active

lwp_manager also comes with some functions to request user stats from lichess.  
All data processing is handled in the bot_fictions.py script. 
