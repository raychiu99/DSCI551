#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson.json_util import dumps
import json
import re
import requests
import certifi
from bson import json_util, ObjectId
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
##MongoDB user
username = "chengrue"
password = "Dsci551"
client = MongoClient("mongodb+srv://{}:{}@551project.l4hb3sd.mongodb.net/mydatabase?retryWrites=true&w=majority".format(username, password), tlsCAFile=certifi.where())
mydatabase = "Project"
# Select the database
db = client.Project
print(db.list_collection_names())



@app.route('/<collection_name>/<key>.json', methods=['PUT', 'PATCH', 'DELETE'])
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
		result = collection.replace_one({'_id': ObjectId(oid)}, data)
		response_data = data
	elif request.method == 'PATCH':
#		name = data["name"]
		document = collection.find_one({"_id": ObjectId(oid)})
		print(document)
		if document:
			result = collection.update_one({'_id': ObjectId(oid)}, {'$set': data})
			response_data = data
		else:
			collection.insert_one(data)
			response_data = data
	elif request.method == 'DELETE':
		result = collection.delete_one({'_id': ObjectId(oid)})
		return jsonify({"deleted_count": result.deleted_count}), 200		
	
	return(json.loads(json_util.dumps(response_data)))

@app.route('/<collection_name>.json', methods=['POST'])
def post_reauest(collection_name):
	collection = db[collection_name]
	jsons = request.get_data().decode('utf-8')
	print(jsons)
	if jsons:
		data = json.loads(jsons)
		print(data,'here')
	response_data = None
	if request.method == 'POST':
		collection.insert_one(data)
		response_data = data
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
			index_name = collection.create_index([(order_by, ASCENDING)])
			print(order_by, index_name)
			indexes = collection.list_indexes()
			print("Indexes in the 'users' collection:")
			for index in indexes:
				print(index["name"])
			if order_by == "$key":
				order_by = "_id"
			elif order_by == "$value":
				return {"error": "Ordering by value is not supported."}, 400
			
			sort_direction = 1
			if "limitToFirst" in query_params:
				limit = int(query_params["limitToFirst"])
			elif "limitToLast" in query_params:
				limit = int(query_params["limitToLast"])
				sort_direction = -1
			else:
				limit = 0
				
			if "equalTo" in query_params:
				filters["name"] = query_params["equalTo"].strip('"')
				
			if "startAt" in query_params:
				filters[order_by] = {"$gte": int(query_params["startAt"].strip('"'))}
				print(filters)
			if "endAt" in query_params:
				if order_by not in filters:
					filters[order_by] = {}
				filters[order_by]["$lte"] = int(query_params["endAt"].strip('"'))
				
			result = collection.find(filters).sort(order_by, sort_direction).limit(limit)
			print(filters,order_by,sort_direction,index_name,limit)
		else:
			result = collection.find(filters)
			
		return(json.loads(json_util.dumps(result)))
	
		
		
		
	
if __name__ == '__main__':
	app.run(debug=True)
	
	