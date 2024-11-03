import os, gridfs, pika, json
from flask import Flask, request
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util

# Create a server
server = Flask(__name__)

# Sever configuation
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/videos"

# Initialize connection to MongoDB and link it to Flask server
mongo = PyMongo(server)

# Initialize GridFS
fs = gridfs.GridFS(mongo.db)

# Configure RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

# Login route
@server.route("/login", methods=["POST"]) 
def login():
    token, error = access.login(request)
    
    if not error:
        return token
    else:
        return None
    
# Upload route
@server.route("/upload", methods=["POST"])
def upload():
    access, error = validate.token(request)
    
    # Deserialize JSON string into python object
    access = json.loads(access)
    
    # Check if user has access (ie; is an admin)
    if access["admin"]:
        if len(request.files) > 1 or len(request.files) < 1:
            return "Only one file can be uploaded", 400
        
        for f in request.files.values():
            error = util.upload(f, fs, channel, access)
        
            if error:
                return error
        
        return "Success!", 200
    else:
        return "Not Authorized!", 401
