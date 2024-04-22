# Manages the database - wipes it for testing and utility purposes

import sqlite3

conn_actions_2 = sqlite3.connect('milk.db');
cursor_actions_2 = conn_actions_2.cursor()

cursor_actions_2.execute("DELETE FROM milk_tracking;")
cursor_actions_2.execute("DELETE FROM daily_counter;")
#cursor_actions_2.execute("DELETE FROM total_counter;")
conn_actions_2.commit()
cursor_actions_2.execute("INSERT INTO daily_counter (count) VALUES (0);")
#cursor_actions_2.execute("INSERT INTO total_counter (count) VALUES (0);")
conn_actions_2.commit()

print("Deleted all entries from table milk_tracking and daily_counter in milk.db")

cursor_actions_2.close()
conn_actions_2.close()

