#============================================================================
#                             Import Statments
#============================================================================

from typing import List, Tuple, Optional
import numpy as np 
from sklearn.metrics.pairwise import cosine_similarity
from database.mongodb import MongoDB
from models.memory import MemoryItem
from datetime import datetime

#============================================================================
#                               Class Statments
#============================================================================

class MemoryStore:
    def __init__(self , database : MongoDB):
        self.database = database

    # -----------------------------------------Add-------------------------------------
    def add_memory_item(self , item : MemoryItem):
        self.database.insert_memory(item)

    # -----------------------------------------Get-------------------------------------
    def get_memory_item_by_id(self , memory_id : str) -> Optional[MemoryItem]:
        data = self.database.get_memory(memory_id)
        if not data:
            return None 
        item = MemoryItem.from_dict(data)
        item.mark_accessed()
        self.database.update_memory(
            memory_id ,
            {
                "last_accessed_timestamp" : item.last_accessed_timestamp,
                "access_count" : item.access_count
            }
        )
        return item 

    # ---------------------------------------Update------------------------------------------
    def update_existing_memory_item(self, memory_id : str , new_text : str , new_embedding , turn_indices : List[int]):
        existing = self.database.get_memory(memory_id)
        if not existing:
            return False 
        old_turn_indices = existing.get("source_turn_indices" , [])
        merged_turn_indices = list(set(old_turn_indices + turn_indices))

        self.database.update_memory(
            memory_id,
            {
                "text" : new_text,
                "embedding" : new_embedding.tolist(),
                "last_accessed_timestamp" : datetime.utcnow(),
                "source_turn_indices" : merged_turn_indices
            }
        )
        return True 

    # ----------------------------------Semantic Search------------------------------------------
    def find_semantically_similar_memories(self,query_embedding , top_k : int = 3 , threshold : float = 0.5) -> List[Tuple[MemoryItem , float]]:
        top_k = int(top_k)
        threshold = float(threshold)
        documents = self.database.get_all_memories()
        if not documents:
            return [] 

        memories = []
        embeddings = [] 

        for document in documents:
            embedding = document.get("embedding")
            if not embedding:
                continue
            try:
                vector = np.array(embedding , dtype=np.float32)
                if vector.size == 0:
                    continue
                memory = MemoryItem.from_dict(document)
                memories.append(memory)
                embeddings.append(vector)
            except Exception as e:
                continue 

        if not embeddings:
            return []

        embedding_matrix = np.vstack(embeddings)
        query_vector = np.array(query_embedding , dtype=np.float32).reshape(1 , -1)
        similarities = (cosine_similarity(query_vector , embedding_matrix)[0])
        sorted_indices = np.argsort(similarities)[::-1]

        results = []

        for index in sorted_indices:
            score = float(similarities[index])
            if score < threshold:
                continue
            results.append(
                (
                    memories[index],
                    score 
                )
            )
            if len(results) >= top_k:
                break 
        return results

    # ------------------------------------------All Memories-----------------------------------------
    def get_all(self):
        documents=  self.database.get_all_memories()
        return [
            MemoryItem.from_dict(document) for document in documents 
        ]

    # ---------------------------------------------Count--------------------------------------------
    def count(self):
        return self.database.count_memories()

    # ---------------------------------------------Clear--------------------------------------------
    def clear(self):
        self.database.clear_memories()

    