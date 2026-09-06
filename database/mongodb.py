#============================================================================
#                                Import Statments
#============================================================================
from typing import Optional
from pymongo import MongoClient
from config.settings import MONGODB_URI,MONGODB_DATABASE,MONGODB_MEMORY_COLLECTION
from models.memory import MemoryItem

#============================================================================
#                                Class Statments
#============================================================================

class MongoDB:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.database = self.client[MONGODB_DATABASE]
        self.collection = self.database[MONGODB_MEMORY_COLLECTION]

    def test_connection(self):
        self.client.admin.command("ping")
        return True 

    def insert_memory(self , memory : MemoryItem):
        self.collection.insert_one(memory.to_dict())

    def get_memory(self , memory_id : str)-> Optional[dict]:
        return self.collection.find_one({
            "memory_id" : memory_id
        })

    def get_all_memories(self):
        return list(self.collection.find({} , { "_id" : 0}))

    def update_memory(self , memory_id : str , update_data : dict):
        self.collection.update_one(
            {
                "memory_id" : memory_id
            },
            {
                "$set" : update_data
            }
        )

    def delete_memory(self , memory_id : str):
        self.collection.delete_one({
            "memory_id" : memory_id
        })

    def count_memories(self):
        return self.collection.count_documents({})

    def clear_memories(self):
        self.collection.delete_many({})
    
    def close(self):
        self.client.close()