#============================================================================
#                             Import Statments
#============================================================================

import json 
from models.memory import MemoryItem
from llm.client import OpenAIClient
from llm.embeddings import EmbeddingService
from llm.prompts import build_memory_update_prompt
from config.settings import SIMILAR_MEMORIES_FOR_UPDATE,MEMORY_SIMILARITY_THRESHOLD
from memory.store import MemoryStore

#============================================================================
#                             Updater Statments
#============================================================================

class MemoryUpdater:
    def __init__(self , memory_store : MemoryStore):
        self.memory_store = memory_store
        self.llm = OpenAIClient()
        self.embeddings = EmbeddingService()

    @staticmethod
    def _parse_json(response_text : str):
        try:
            start = response_text.find("{")
            end = response_text.rfind("}")

            if(start == -1 or end == -1 or end < start):
                return {
                    "operation" : "NOOP"
                }
            json_text = response_text[start : end + 1]
            result = json.loads(json_text)

            if not isinstance(result , dict):
                return {
                    "operation" : "NOOP"
                }
            return result
        except(json.JSONDecodeError , TypeError):
            return {
                "operation" : "NOOP"
            }

    def decide_operation(self , fact : str , similar_memories):
        if not similar_memories:
            similar_memory_text = "No Similar memories found."
        else:
            lines = []
            for index , (memory , score) in enumerate(similar_memories , start=1):
                lines.append(f"""
                    {index}.
                    Memory ID: {memory.id}
                    Similarity : {score:.4f}
                    Text : {memory.text}
                """)

                similar_memory_text = (
                    "\n".join(lines)
                )

        prompt = build_memory_update_prompt(candidate_fact=fact , similar_memories=similar_memory_text)
        response = self.llm.chat([
            {"role" : "system" , "content" : "Return only valid JSON"},
            {"role" : "user" , "content" : prompt}
        ], temperature=0)

        return self._parse_json(response['content'])
        

    # --------------------------------Process Fact--------------------------------
    def _process_fact(self , fact : str , turn_index : int):

        # Create embedding
        fact_embedding = self.embeddings.get_embedding(fact)

        # Search similar memories
        similar_memories = self.memory_store.find_semantically_similar_memories(query_embedding=fact_embedding , top_k=SIMILAR_MEMORIES_FOR_UPDATE , threshold=MEMORY_SIMILARITY_THRESHOLD)

        # Ask GPT what to do
        decision = self.decide_operation(fact , similar_memories)
        operation = decision.get("operation" , "NOOP").upper()

        # Add
        if operation == "ADD":
            memory = MemoryItem(
                text=fact,
                embedding=fact_embedding.tolist(),
                source_turn_indices=[turn_index]
            )
            self.memory_store.add_memory_item(memory)
            return {
                "operation" : "ADD",
                "memory_id" : memory.id,
                "fact" : fact 
            }

        # Update 
        if operation == "UPDATE":
            target_memory_id = decision.get("target_memory_id")
            updated_memory_text = decision.get("updated_memory_text")

            if(target_memory_id and updated_memory_text):
                updated_embedding = self.embeddings.get_embedding(updated_memory_text)
                success = self.memory_store.update_existing_memory_item(
                    memory_id=target_memory_id,
                    new_text=updated_memory_text,
                    new_embedding=updated_embedding,
                    turn_indices=[turn_index]
                )

                if success:
                    return {
                        "operation" : "UPDATE",
                        "memory_id" : target_memory_id,
                        "fact" : updated_memory_text
                    }

        #  NOOP
        return {
            "operation" : "NOOP",
            "fact" : fact 
        }
    