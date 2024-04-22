# Bash file to run on startup, automatically starts required programs whenever Pi restarts

#!/bin/bash

# Navigates to the proper directory
cd /home/racer

# Generates a timestamp for the logfile name               
#timestamp=$(date +"%Y%m%d_%H%M%S")

# Creates a unique log file based on the timestamp of startup
#log_file = "/home/racer/LogFiles/logfile_$(timestamp).log"

# Redirect both stdout and stderr to a log file
#exec > $"log_file" 2>&1

# Activate virtual environment
source milk_env/bin/activate

# Run Flask app
python app.py &

# Run actions.py
python actions.py &

# Keep terminal open until user presses enter
read -p "Press Enter to exit"