# Generates the tweet - separate file for cleanliness.

from datetime import datetime
import random
import sqlite3

# Function to get the current time in HH:MM form
def get_time():
	current_time = datetime.now()
	formatted_time = current_time.strftime("%H:%M")
	print("Current time: " + str(formatted_time))
	return formatted_time;
	
# Function to get the total count
def get_total_count():
	conn_tweet = sqlite3.connect('milk.db')
	cursor_tweet = conn_tweet.cursor()
	count = ""
	try:
		cursor_tweet.execute("SELECT count FROM total_counter ORDER BY count DESC LIMIT 1;")
		count = str(cursor_tweet.fetchone()[0])
		print("Total count fetched: " + count)
	except Exception as e:
		print(f"Error: {e}")
		count = "N/A"
	finally:
		cursor_tweet.close()
		conn_tweet.close()
      
	return str(count)
    
# Stores all the potential tweets in a dictionary organized by how many 
	# glasses of milk he's had 
tweet_string = {
	'1': [
		  "First glass of milk of the day. Wow. Only took until {time}, wow. Hope it was worth it, asshole. Total count: {total_count}",
		  "Hear ye, hear ye! It's currently {time} and we have our first milk of the day! Maybe if we're lucky he chokes on it! Total count: {total_count}", 
		  "Milk #1 of the day is at {time}. God help us. Total: {total_count}",
		  "The first glass of milk has been logged at {time}. Total count: {total_count}",
		  "There appears to be no end to this Hell, as he has once again taken pleasure in a glass of milk - his first of the day, being at {time}. Total count: {total_count}",
		  "Just now ({time}), a glass of milk was poured. At the same time, God winces as he looks down at us - for there is no greater sin to humanity than what this man is doing to our milk supply. Total count: {total_count}",
		  "{time}. {time}. {time}. THE HOUR OF THE FIRST MILKENING. PLEASE, GOD, MAKE IT STOP. TOTAL COUNT: {total_count}",
		  "I regret to inform the general public that our subject has decided to drink milk on this beautiful new day at {time}. Total count: {total_count}",
		  "The ricin that I put in the milk yesterday did not work, apparently. A new day, a new glass of milk, at {time}! Total count: "
		 ],
	'2': [
			"Milk counter on the day has just hit 2 at {time}. Total: {total_count}",
			"Wow, a second glass of milk - what a surprise! And at {time} too...that's an interesting time to drink milk... Total count: {total_count}",
			"Glass #2 of the day comes at {time}. Shame on you. Total count: {total_count}",
			"Looks like someone's a little thirsty...for MILK! Haha! Because he just drank his SECOND glass of milk. It's {time} and that's just too many glasses for today. Total count: {total_count}",
			"The second glass of milk of the day has been logged at {time}. Total count: {total_count}",
			"Glass two of the day comes at {time}. Total count: {total_count}",
			"Mr. President...at {time}, he drank a second glass of milk. Total: {total_count}"  
			],
	'3': [
			"THREE. THREE GLASSES OF MILK TODAY HAS JUST BEEN HIT AT {time}. WHAT THE FUCK??? TOTAL: {total_count}",
			"At {time}, the fridge was opened and the milk was removed - for the THIRD TIME today. THAT IS TOO MUCH MILK. Total count: {total_count}",
			"Glass #3 of the day comes at {time}. Why three? That's too many. Milk tastes good. But...really? This is just getting ridiculous. Total: {total_count}"
		 ],
	'4': [
			"{time} marks four glasses of milk. I do not have anything witty to say. This is just too much milk. Do you see why I made this now? Total: {total_count}",
			"GLASS NUMBER FOUR. {time}. FOUR GLASSES TODAY ALONE. I NO LONGER FEEL SAFE IN THIS APARTMENT, ESPECIALLY NOT WITH A TOTAL COUNT OF {total_count}",
			"{time}. #4. Total: {total_count}" + " (There's nothing witty to say here. I am too busy moving out should this message ever be sent."
		 ],
	'5': [
			"CRITICAL MILK LEVELS. {time} MARKS #5 ON THE DAY. GOD HAS ABANDONED THIS APARTMENT AND IT WAS MY ROOMMATE WHO BANISHED HIM.",
			"HELP HELP HELP HELP HELP HELP HELP HELP HELP IF YOU ARE SEEING THIS THERE HAVE BEEN FIVE GLASSES OF MILK TODAY. HELP HELP HELP HELP HELP HELP HELP",
			"AT THIS POINT, YOU ARE IN DANGER TOO. FIVE GLASSES OF MILK HAVE BEEN REACHED AT {time}. THERE IS NOTHING WE CAN DO TO SAVE OURSELVES NOW."
		 ],
	'-1': [ 
			"It's a new day! The code has been announced, and we await in silence for the next shameful glass. May today's counter be less than yesterday's and we find peace in this never-ending milky Hellscape."
		  ],
}



# Fail safe. May God hope we never see it.
max_tweet = "This is a warning. There are over five glasses of milk today ALONE. Should this tweet ever be posted, know that I am in the process of moving out and the authorities have been alerted. Thank you for your time and may God help us all."

def get_tweet_string(count):
	print("Tweet string program being generated with daily_counter value of " + str(count))
	selected_array = tweet_string.get(str(count), [])
	tweet = random.choice(selected_array) if selected_array else max_tweet
	if(count == -1):
		random_spaces = random.randint(1, 10)
		tweet += ' ' * random_spaces
	curr_time = get_time()
	curr_total_count = get_total_count()
	formatted_tweet = tweet.format(time=curr_time, total_count=curr_total_count)
	return formatted_tweet
