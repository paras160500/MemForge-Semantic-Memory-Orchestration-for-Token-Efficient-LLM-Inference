#============================================================================
#                             Import Statments
#============================================================================
import numpy as np 
from openai import OpenAI
from config.settings import OPENAI_API_KEY , OPENAI_EMBEDDING_MODEL, OPENAI_EMBEDDING_DIMENSIONS

#============================================================================
#                               Logic Statments
#============================================================================
class EmbeddingService:

    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model = OPENAI_EMBEDDING_MODEL
        self.dimensions = OPENAI_EMBEDDING_DIMENSIONS

    def get_embedding(self , text : str) -> np.ndarray:
        response = self.client.embeddings.create(model = self.model , input=text , dimensions=self.dimensions)
        embedding = response.data[0].embedding
        return np.array(embedding , dtype=np.float32)

    def get_embedding_dimensions(self):
        return self.dimensions