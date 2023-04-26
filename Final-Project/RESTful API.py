#!/usr/bin/env python3

from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Resource, Api
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
import json
import re
import requests
import certifi
from bson import json_util, ObjectId
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
app = Flask(__name__)
CORS(app)
#socketio = SocketIO(app)
socketio = SocketIO(app, cors_allowed_origins="*")
##MongoDB user
username = "chengrue"
password = "Dsci551"
client = MongoClient("mongodb+srv://{}:{}@551project.l4hb3sd.mongodb.net/mydatabase?retryWrites=true&w=majority".format(username, password), tlsCAFile=certifi.where())
mydatabase = "Project"
# Select the database
db = client.Project
print(db.list_collection_names())

@app.route('/<collection_name>/<int:key>.json', methods=['PUT', 'PATCH', 'DELETE'])
def handle_request(collection_name,key):
#	collection_name = re.split('[./]', path)[0]
	oid = key
	print(collection_name,key)
	collection = db[collection_name]
	param = request.args
	params = {key: int(value) if value.isnumeric() else value.strip('"') for key, value in param.items()}
	print(params)
	jsons = request.get_data().decode('utf-8')
	print(jsons)
	if jsons:
		data = json.loads(jsons)
		print(data,'here')
	response_data = None
	
	if request.method == 'PUT':
		document = collection.find_one({"_id": oid})
		print(document)
		if document:
			result = collection.replace_one({'_id': oid},data)
		else:
			collection.update_one({'_id': oid}, {'$set': data}, upsert=True)
			
		
		response_data = data
		socketio.emit('data_updated', {'event': 'updated', 'data': data})
	elif request.method == 'PATCH':
#		name = data["name"]
		document = collection.find_one({"_id": oid})
		print(document)
		if document:
			result = collection.update_one({'_id': oid}, {'$set': data}, upsert=True)
			response_data = data
			socketio.emit('data_updated', {'event': 'created', 'data': data})
		else:
			collection.update_one({'_id': oid}, {'$set': data}, upsert=True)
			response_data = data
			socketio.emit('data_updated', {'event': 'updated', 'data': data})
	elif request.method == 'DELETE':
		result = collection.delete_one({'_id': oid})
		socketio.emit('data_updated', {'event': 'deleted', 'user_id': oid})
		return jsonify({"deleted_count": result.deleted_count}), 200		
	
	return(json.loads(json_util.dumps(response_data)))

@app.route('/<collection_name>.json', methods=['POST'])
def post_request(collection_name):
	collection = db[collection_name]
	jsons = request.get_data().decode('utf-8')
	#print(jsons)
	if jsons:
		data = json.loads(jsons)
		print(data,'here')
	response_data = None
	if request.method == 'POST':
		collection.insert_one(data)
		response_data = data
	socketio.emit('data_updated', {'event': 'created', 'data': data})
	return(json.loads(json_util.dumps(response_data))) 

@app.route('/<collection_name>.json', methods=['GET'])
def get_request(collection_name):
#	collection_name = re.split('[./]', path)[0]
	print(collection_name)
	collection = db[collection_name]
	query_params = request.args
	print(query_params)
	filters = {}
	
	if request.method == 'GET':
		if "orderBy" in query_params:
			order_by = query_params["orderBy"].strip('"')
			if order_by != "$key" and order_by != "$value":
				index_name = collection.create_index([(order_by, ASCENDING)])
				print(order_by, index_name)
				indexes = collection.list_indexes()
			if order_by == "$key":
				order_by = "_id"
			elif order_by == "$value":
				indexes = collection.list_indexes()
				if indexes is None:
					return {"error": "Ordering by value is not supported. There's no index created"}, 400
				print("Indexes in the 'users' collection:")
				indexes = collection.index_information()
				key = list(indexes.keys())[1]
				order_by = key.split("_")[0]
				print(order_by)
			
			sort_direction = 1
			if "limitToFirst" in query_params:
				limit = int(query_params["limitToFirst"])
			elif "limitToLast" in query_params:
				limit = int(query_params["limitToLast"])
				sort_direction = -1
			else:
				limit = 0
				
			if "equalTo" in query_params:
				equalTo_value = query_params["equalTo"].strip('"')
				if equalTo_value.isdigit():
					filters[order_by] = int(equalTo_value)
				else:
					filters[order_by] = equalTo_value
#				filters[order_by] = query_params["equalTo"].strip('"')
				
			if "startAt" in query_params:
				filters[order_by] = {"$gte": int(query_params["startAt"].strip('"'))}
#				print(filters)
			if "endAt" in query_params:
				if order_by not in filters:
					filters[order_by] = {}
				filters[order_by]["$lte"] = int(query_params["endAt"].strip('"'))
				
			result = collection.find(filters).sort(order_by, sort_direction).limit(limit)
#			print(filters,order_by,sort_direction,limit)
		else:
			result = collection.find(filters)
#		print(list(result))
		return(json.loads(json_util.dumps(result)))
@app.route('/')
def index():
    with open('index.html', 'r') as file:
        html = file.read()
    return html

@app.route('/static/<path:path>')
def serve_static(path):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static'), path)	

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('user_created')
def handle_user_created(data):
    emit('new user created', data, broadcast=True)

@socketio.on('user_updated')
def handle_user_updated(data):
    emit('user updated', data, broadcast=True)

@socketio.on('user_deleted')
def handle_user_deleted(data):
    emit('user deleted', data, broadcast=True)

if __name__ == '__main__':
	#app.run(debug=True)
	socketio.run(app, debug=True,host='127.0.0.1', port=5000)
	
	
	
	