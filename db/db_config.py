from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(
    host="localhost",
    port=27017,
)
db = client["RLTest"]
start_collection = db["sample_collection"]
