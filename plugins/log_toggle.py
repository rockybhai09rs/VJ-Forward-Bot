from pymongo import MongoClient
from config import Config

client = MongoClient(Config.MONGO_URL)
db = client["vj_forward"]
log_pref = db["log_pref"]

async def is_log_enabled(user_id: int) -> bool:
    data = log_pref.find_one({"_id": user_id})
    return data.get("enabled", True) if data else True

async def toggle_log(user_id: int) -> bool:
    current = await is_log_enabled(user_id)
    new_status = not current
    log_pref.update_one({"_id": user_id}, {"$set": {"enabled": new_status}}, upsert=True)
    return new_status
