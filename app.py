# Flask server that watches for POSTs and adds information to DB accordingly

from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

def insert_to_database(value, timestamp):
	# Connecting to database
	conn = sqlite3.connect('milk.db')
	cursor = conn.cursor()
	# Inserts sensor data into the table
	query = "INSERT INTO milk_tracking (value, timestamp) VALUES (?, ?)"
	cursor.execute(query, (value, timestamp))
	conn.commit()
	
@app.route('/')
def hello():
	return 'wwwweb serverrrrrr'
	
@app.route('/add_data', methods=['POST'])
def add_data():
	try:
		data = request.get_json()
		value = data['value']
		timestamp = data['timestamp']
	
		# Inserts data into database
		insert_to_database(value, timestamp)
		
		return jsonify({"status": "success", "message": "Data added successfully!"})
	except Exception as e:
		return jsonify({"status": "error", "message": str(e)})
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=50005)
	
	
