# ONLY WORKS ON WINDOWS
# Script to block connecting IPs if they match a BYOND DOS attempt
# Original JS Script by monster860
# Converted to python by AffectedArc07

# Imports
import time, os, sqlite3, sys, re, subprocess

# Generate DB connection for caching of blocked IPs
db = sqlite3.connect("Data.db")
cur = db.cursor()

# CONFIGURATION #
os.chdir("W:/Configuration/GameStaticFiles/data/logs") # Set the parameter below to your server log root. USE EXACT PATHS
ddLogName = "runtime.log" # Set this to the name of your DD log file
useOldSystem = False # Set this to True if your log path if logs/year/month/day instead of logs/year/month/day/round-id
configured = False # Set this to True once you have configured this file

# Vars, dont touch
ddLogPath = ""
lastLine = ""
matchingRegex = re.compile("^\\[2\\d\\d\\d-[0-1][0-9]-[0-3][0-9] [0-2][0-9]:[0-6][0-9]:[0-6][0-9].[0-9]+] Possible denial of service attempt from ([0-9\.]+)$") # Define this now so its not wasting CPU re-defining it

# Now for the actual code

# Function to handle an IP
def handle_ip(ip):
    cur.execute("SELECT ip FROM cache WHERE ip=?",(ip,))
    IPcheck = cur.fetchone()
    if IPcheck: # IP is already in the database, move on
        return

    # If we are here, we have an IP to block
    os.system("netsh advfirewall firewall add rule name=\"DoS Block " + str(ip) + "\" dir=in interface=any action=block remoteip=" + str(ip) + "/32")
    # With the rule added, lets update the DB
    cur.execute("INSERT INTO cache (ip) VALUES (?)",(ip,))
    db.commit()
    print("Successfully blocked IP: "+str(ip))


# Function to actually check lines
def handle_line(line):
    global matchingRegex
    matchFound = matchingRegex.match(line)
    if matchFound:
        handle_ip(matchFound[1])


# Function to get the last (most recent) dir in a directory
def get_last_dir(dir):
    dirs = []
    for x in os.scandir(dir):
        if x.is_dir():
            dirs.append(x.path)

    dirs.sort(reverse=True)
    return dirs[0]

# Updates the current DD log for tracking purposes
def update_dd_log():
    global ddLogPath
    if useOldSystem: # Doesnt need an extra getLastDir
        newLogPath = get_last_dir(get_last_dir(get_last_dir(os.getcwd())))
    else:
        newLogPath = get_last_dir(get_last_dir(get_last_dir(get_last_dir(os.getcwd()))))

    # If the path is the same, then return
    if ddLogPath == newLogPath:
        return
    # Otherwise, do shit
    ddLogPath = newLogPath

# Checks if lines have changed, and if they have, handle them
def update_lines():
    global ddLogName, ddLogPath, lastLine
    logFile = open(str(ddLogPath)+"\\"+str(ddLogName), "r")
    lines = logFile.readlines()
    logFile.close()

    # If the last line is the same, the file hasnt changed, so return
    if lastLine == lines[-1]:
        return
    # Otherwise, its time to work
    lastLine = lines[-1]

    for line in lines: # Now we do actual matching
        handle_line(line)

        


# Check for config
if not configured:
    print("ERROR: File is not configured. Please configure this file before running")
    sys.exit(1)
else:
    print("Config loaded")

# Check for valid DB schema
try:
    cur.execute("SELECT * FROM cache")
except sqlite3.OperationalError:
    print("ERROR: DB Schema not initialized. Please run Generate-DB.py")
    sys.exit(1)

print("Script successfully loaded. Will execute every minute")

# Now run
while True:
    update_dd_log()
    update_lines()
    time.sleep(60) # Sleeps for 1 minute.
