from gridfs import GridFS
from pymongo import MongoClient

def get_database():
    CONNECTION_STRING = "mongodb+srv://crsongirkar2:Chinmay@08@cluster0.r5z90ei.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(CONNECTION_STRING)
    db = client['plag_check']
    fs = GridFS(db)
    return client, db, fs

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    # Get the database
    client, db, fs = get_database()
