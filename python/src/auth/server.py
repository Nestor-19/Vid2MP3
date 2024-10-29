import jwt, datetime, os
from flask import Flask, request
from flask_mysqldb import MySQL

# Create a server
server = Flask(__name__)

# Allow app to connect to and query MySQL database
mysql = MySQL(server)

# Sever configuation
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

# Login route
@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing Credentials", 401
    
    # Verify username and password in DB
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s", (auth.username)
    )
    
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]
        
        # Validate user
        if auth.username != email or auth.password != password:
            return "Invalid Credentials!", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        # User does not exist in DB
        return "Invalid Credentials!", 401

def createJWT(username, secret, is_admin):
    return jwt.encode(
        {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": is_admin
        },
        secret,
        algorithm="HS256"
    )
    