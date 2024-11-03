import pika, json

# Handle uploading the file to MongoDB
def upload(file, fs, channel, access):
    try:
        fid = fs.put(file)
    except:
        return "Internal Server Error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"]
    }
    
    # Upon a successful upload, put a message on the queue
    try:
        channel.basic_publish(
            exchange="",
            routing_key="video",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE
            ),  
        )
    except:
        # Delete the file from mongoDB as it will never get processed
        # due to not having a respective message on the queue
        fs.delete(fid)
        return "Internal Server Error", 500
    