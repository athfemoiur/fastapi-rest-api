import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)

db = client['fastapi']