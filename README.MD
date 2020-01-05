# BYOND IP Blocker
This script searched BYOND dream daemon logs for DOS attempts, and then blocks the IPs in windows firewall. It is based off of a script written by monster860.

Requires Python 3

# How To Install
1. Run `Generate-DB.py` to generate a sqlite3 .db file which will store which IPs are blocked
2. Launch `IP-Blocker.py` **AS ADMINISTRATOR**
3. Make a coffee