from flask import Flask, jsonify, request
from flask_socketio import SocketIO, emit
from pymongo import MongoClient
from bson.objectid import ObjectId
import subprocess
import sys
import os

# def run_cli():
#     cli_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cli.py')
#     subprocess.Popen([sys.executable, cli_script])

app = Flask(__name__)
socketio = SocketIO(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['my_database'] 
collection = db['users']

@app.route('/')
def index():
    return "Welcome to the Firebase!"

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        cursor = collection.find()
        users = [user for user in cursor]
        return jsonify(users)
    elif request.method == 'POST':
        user_data = request.json
        result = collection.insert_one(user_data)
        socketio.emit('data_updated', {'event': 'created', 'data': user_data})
        return jsonify({"success": True, "message": "User created", "_id": str(result.inserted_id)})

@app.route('/users/<int:user_id>', methods=['PUT', 'PATCH', 'DELETE'])
def user(user_id):
    print(f"Request received: method={request.method}, user_id={user_id}")
    #oid = ObjectId(user_id)
    oid = user_id
    if request.method == 'PUT':
        user_data = request.json
        result = collection.replace_one({'_id': oid}, user_data)
        if result.modified_count == 1:
            #socketio.emit('data_updated', {'event': 'updated', 'data': user_data}, broadcast=True)
            socketio.emit('data_updated', {'event': 'updated', 'data': user_data})
            return jsonify({"success": True, "message": "User updated"})
        else:
            return jsonify({"success": False, "message": "User not found"})
    elif request.method == 'PATCH':
        update_data = request.json
        result = collection.update_one({'_id': oid}, {'$set': update_data})
        print(f"Query filter: {{'_id': {user_id}}}")  # Debug print
        print(f"Result: {result.raw_result}")  # Debug print

        if result.modified_count == 1:
            #socketio.emit('data_updated', {'event': 'updated', 'data': update_data}, broadcast=True)
            socketio.emit('data_updated', {'event': 'updated', 'data': update_data})
            return jsonify({"success": True, "message": "User updated"})
        else:
            return jsonify({"success": False, "message": "User not found"})
    elif request.method == 'DELETE':
        result = collection.delete_one({'_id': oid})
        if result.deleted_count == 1:
            #socketio.emit('data_updated', {'event': 'deleted', 'user_id': user_id}, broadcast=True)
            socketio.emit('data_updated', {'event': 'deleted', 'user_id': user_id})
            return jsonify({"success": True, "message": "User deleted"})
        else:
            return jsonify({"success": False, "message": "User not found"})

if __name__ == '__main__':
    # run_cli()
    socketio.run(app, debug=True)
