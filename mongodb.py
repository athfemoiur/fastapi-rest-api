import motor.motor_asyncio
from decouple import config

# client for async connection to mongo

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = client[config('DB_NAME')]
