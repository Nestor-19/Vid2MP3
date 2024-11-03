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

# Initialize Gr idFS
fs = gridfs.GridFS(mongo.db)

# Configure RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

# Login route
@server.route("/login", methods=["POST"]) 
def login():
    token, error = access.login(request)