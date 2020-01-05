import sqlite3, sys

confirm = input("Are you SURE you want to re-create the DB schema? ALL CACHE DATA WILL BE LOST!!! Type \"YES\" if so: ")

if confirm != "YES":
    print("Operation aborted")
    sys.exit()

# Now make the DB schema
db = sqlite3.connect("Data.db")
cur = db.cursor()
cur.execute("DROP TABLE IF EXISTS cache")
cur.execute("CREATE TABLE 'cache' ('ip' TEXT, PRIMARY KEY('ip'))")
db.commit()
cur.close()
db.close()
input("Process complete. Press enter to close")

