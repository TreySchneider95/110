import pymongo
import certifi
from dotenv import load_dotenv
import os



load_dotenv()
url = str(os.getenv('mongo_url'))

client = pymongo.MongoClient(url, tlsCAFile=certifi.where())
db = client.get_database("socks4u")