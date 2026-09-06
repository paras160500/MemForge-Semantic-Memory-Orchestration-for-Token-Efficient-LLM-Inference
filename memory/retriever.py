#============================================================================
#                             Import Statments
#============================================================================

from llm.embeddings import EmbeddingService
from config.settings import MEMORY_RETRIEVAL_TOP_K , MEMORY_SIMILARITY_THRESHOLD
from memory.store import MemoryStore

#============================================================================
#                             REtriever Statments
#============================================================================

class MemoryRetriever:

    def __init__(self , memory_store : MemoryStore):
        self.memory_store = memory_store
        self.embeddings = EmbeddingService()

    def retrieve(self , query : str , top_k : int = MEMORY_RETRIEVAL_TOP_K):
        query_embedding = self.embeddings.get_embedding(query)
        memories = self.memory_store.find_semantically_similar_memories(
            query_embedding=query_embedding,
            top_k=top_k,
            threshold=MEMORY_SIMILARITY_THRESHOLD
        )
        return memories

    def format_memories(self , memories):
        if not memories:
            return "No relevant memories found."

        lines = []

        for index , (memory , score) in enumerate(memories , start=1):
            lines.append(f"{index}. {memory.text}")

        return "\n".join(lines)