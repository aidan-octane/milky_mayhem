# Constantly-running threaded program that acts as the central figure
# for any actions upon any events - the tweets whenever the database is 
# updated, the actions at midnight, etc. 

import schedule
import time
import threading
import sqlite3
import tweepy
import random
from tweet_string import get_tweet_string
from pydub import AudioSegment
from pydub.playback import play


# Connects to Twitter API
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

client = tweepy.Client(
    consumer_key=consumer_key, consumer_secret=consumer_secret,
    access_token=access_token, access_token_secret=access_token_secret
)

# Connection to the database :D

conn = sqlite3.connect('milk.db');

# Stores the current number of entries in table in counter
# Also grabs the last known entry 
last_known_entry = ""
cursor_begin = conn.cursor()

try:
    cursor_begin.execute("SELECT * FROM daily_counter;")
    daily_counter = (int)(cursor_begin.fetchone()[0])
    print("Daily counter determined to be " + str(daily_counter))
    cursor_begin.execute("SELECT timestamp FROM milk_tracking ORDER BY timestamp DESC LIMIT 1;")
    last_known_entry = str(cursor_begin.fetchone())
    print("Last known entry: " + last_known_entry)
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor_begin.close()
    conn.close()

# Increments total counter in db
def increment_total():
    conn_increment_total = sqlite3.connect('milk.db')
    cursor_increment_total = None
    try:
        cursor_increment_total = conn_increment_total.cursor()
         # Increment the count by 1
        cursor_increment_total.execute("UPDATE total_counter SET count = count + 1;")
        conn_increment_total.commit()
        cursor_increment_total.execute("SELECT count FROM total_counter ORDER BY count DESC LIMIT 1;")
        count = cursor_increment_total.fetchone()[0] 
        print("Total counter incremented: now is " + str(count)) 
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cursor_increment_total:
            cursor_increment_total.close()
        else:
            print("Error with cursor_increment")
        conn_increment_total.close()

        
# Manipulates daily_counter variable
def manipulate_counter(mode):
    conn_counter = sqlite3.connect('milk.db')
    cursor_counter = conn_counter.cursor()
    # If mode = 1, then it was called by 'monitor_entries' - else, it was called by actions_at_midnight
    if mode == 1:
        cursor_counter.execute("UPDATE daily_counter SET count = count + 1;")
    else : 
        cursor_counter.execute("UPDATE daily_counter SET count = 0;")
    conn_counter.commit()
    cursor_counter.close()
    conn_counter.close()

# Gets value of daily_counter variable, used because global variables within the threads are giving issues
def get_daily_counter(): 
    conn_get_counter = sqlite3.connect('milk.db')
    cursor_get_counter = conn_get_counter.cursor()
    cursor_get_counter.execute("SELECT count FROM daily_counter;")
    daily_counter = int(cursor_get_counter.fetchone()[0])
    cursor_get_counter.close()
    conn_get_counter.close()
    return daily_counter
        

def declare():
    file_path = "/home/racer/Desktop/Audios/"
    file_name = ""
    count = get_daily_counter()
    if(count < 6):
        file_first_digit = str(count)
        random_number = random.randint(1, 5)
        #random edge case cause i messed up audio 32
        while(file_first_digit == '3' and random_number == 2):
            random_number = random.randint(1, 5)
        file_name = file_path + file_first_digit + str(random_number) + ".mp3"
    else:
        file_name = file_path + "X.mp3"
    # plays the Sound
    print("Playing sound: " + file_name);
    audio = AudioSegment.from_file(file_name, format="mp3")
    play(audio)
    
# Calls the twitter API to tweet out the timestamp of the latest milk
def callTwitterAPI(mode):
    # Gets tweet from other file based off of the daily counter of milks
    if(mode == 1):
        tweet = get_tweet_string(get_daily_counter())
    else:
        tweet = get_tweet_string(-1)
    print("Tweeting out the following: " + str(tweet))
    response = client.create_tweet(
        text=tweet
    )
    print(f"https://twitter.com/user/status/{response.data['id']}")

    
def actions_at_midnight():
    print("Scheduler determined it to be midnight! Executing actions:")
    current_local_time = time.localtime()
    # Plays the Declaration
    if current_local_time.tm_hour == 23 and current_local_time.tm_min == 59:
        print("Time check passed")
        declare()
    else:
        print("Debugging stopped wrongful execution of declaration")
    # Makes tweet
    # try:
      #  callTwitterAPI(0)
    # except Exception as e:
      #  print("ERROR CREATING TWEET")
        
    # Deletes every entry from the table and starts anew:
    # Connect to the SQLite database
    conn_actions = sqlite3.connect('milk.db');
    cursor_actions = conn_actions.cursor()
    try:
        # Delete all entries from the 'your_table_name' table
        cursor_actions.execute("DELETE FROM milk_tracking;")
        conn_actions.commit()

        print("All entries deleted at midnight")
        # Sets daily_counter to 0 
        manipulate_counter(0)

    except Exception as e:
        print(f"Error deleting entries: {e}")

    finally:
        # Close the cursor
        cursor_actions.close()
        conn_actions.close()
        

def monitor_new_entries(entry):
    latest_entry=""
    known_latest_entry = entry
    i = 0
    print("Monitoring thread began!")
    while True:
        if(i < 3):
                print(".")
                i = i + 1;
        else:
                print("Checking for new updates to database - last known entry is " + known_latest_entry)
                i = 0;
            
        # Connect to the SQLite database
        conn_monitor = sqlite3.connect('milk.db');
        cursor_monitor = conn_monitor.cursor()
        try:
            # Grabs latest entry in database
            cursor_monitor.execute("SELECT timestamp FROM milk_tracking ORDER BY timestamp DESC LIMIT 1;")
            latest_entry = str(cursor_monitor.fetchone())
            # Checks for changes in database
            # Also could just count # of entries and if it goes up
            if latest_entry != known_latest_entry:
                if(latest_entry != 'None'):
                    print("New entry detected: ", latest_entry)
                    # Update daily_counter by adding one
                    print("Updating daily counter:")
                    manipulate_counter(1)
                    print("Daily counter updated. Updating total counter:")
                    # Updates total counter 
                    increment_total()
                    print("Daily counter is now: " + str(get_daily_counter()))
                     # Set 'last known entry' to be the latest entry 
                    print("Resetting last known entry...")
                    known_latest_entry = latest_entry
                    print("Last known entry reset to " + known_latest_entry)
                    # Call Twitter API
                    callTwitterAPI(1)
                    
                   
        except Exception as e:
            print(f"Error monitoring new entries: {e}")

        finally:
            # Close the database connection
                cursor_monitor.close()
                conn_monitor.close()
        # Check for new entries every 10 seconds (adjust as needed)
        time.sleep(10)
        
        
# Schedule the task to run every day at midnight
schedule.every().day.at("23:59").do(actions_at_midnight)

# Function to run the scheduled tasks in a separate thread
def run_scheduler():
    print("Scheduler thread began!")
    while True:
        schedule.run_pending()
        time.sleep(1)

# Creates and starts the scheduler thread
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

# Creates and starts the thread for monitoring new entries
monitor_thread = threading.Thread(target=monitor_new_entries,
                    args=(last_known_entry,))

monitor_thread.start()
