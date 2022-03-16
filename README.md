# watch party emcee
keep an eye out on who's currently playing games on lichess

need a mysql db called watch_lichess 
with a table called watch_users
table should have two columns: handle(varchar) and status(bool)

emcee.py grabs all users from the table, than asks lichess about their current status, and updates table
this db does not keep history, just current status

emcee.py is intended to be run by a scheduler, probably every 3 minutes
