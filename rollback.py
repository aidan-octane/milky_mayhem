# "Rolls back" the database by one in the event of an error
import sqlite3

# Removes entry from milk_tracking without triggering actions.py 
# De-increments daily_counter
# De-increments total_counter

conn_rollback = sqlite3.connect('milk.db');
cursor_rollback = conn_rollback.cursor()

# Removes last entry from milk_tracking - warning, will trigger the actions
# cursor_actions.execute("DELETE FROM milk_tracking WHERE timestamp = (SELECT MAX(timestamp) FROM milk_tracking);")

# Remove 1 from daily counter (which works by just inserting a new incremented count rather than just having a 1-item database)
cursor_rollback.execute("UPDATE daily_counter SET count = (SELECT * FROM daily_counter) - 1;")
conn_rollback.commit()
cursor_rollback.execute("SELECT count FROM daily_counter ORDER BY count DESC LIMIT 1;")
dailycounter = cursor_rollback.fetchone()
print("Removed 1 from daily counter - now is: " + str(dailycounter))

# De-increments total_counter
cursor_rollback.execute("UPDATE total_counter SET count = (SELECT * FROM total_counter) - 1;")
conn_rollback.commit()
cursor_rollback.execute("SELECT count FROM total_counter ORDER BY count DESC LIMIT 1;")
totalcounter = cursor_rollback.fetchone()
print("Removed 1 from total counter - now is: " + str(totalcounter))

cursor_rollback.close()
conn_rollback.close()

