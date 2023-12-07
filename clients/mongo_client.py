from dotenv import load_dotenv
from mongoengine import Document, connect
import os

load_dotenv()

mongodb_uri = os.getenv("MONGO_DB_CONN_STRING")
connect(host=mongodb_uri)


# MongoDB Connections are lazzy in nature
# creating a test document and running object_count method to make sure connection is made.
class Test(Document):
    pass


def connect_mongo_db():
    try:
        Test.objects.count()
        print("Connection to MongoDB Successful")
    except Exception as e:
        print(f"Connection failed: {e}")
