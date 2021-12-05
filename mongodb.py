import motor.motor_asyncio

# client for async connection to mongo

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = client['fastapi']