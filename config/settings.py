#============================================================================
#                                Import Statments
#============================================================================
import os 
from dotenv import load_dotenv
load_dotenv()

#============================================================================
#                                 Env Statements
#============================================================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL")

OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL")
OPENAI_EMBEDDING_DIMENSIONS = os.getenv("OPENAI_EMBEDDING_DIMENSIONS")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE")
MONGODB_MEMORY_COLLECTION = os.getenv("MONGODB_MEMORY_COLLECTION")

MEMORY_SIMILARITY_THRESHOLD = os.getenv("MEMORY_SIMILARITY_THRESHOLD" , "0.5")
MEMORY_RETRIEVAL_TOP_K = os.getenv("MEMORY_RETRIEVAL_TOP_K" , "3")
SIMILAR_MEMORIES_FOR_UPDATE = os.getenv("SIMILAR_MEMORIES_FOR_UPDATE" , "3")


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not available")

if not MONGODB_URI:
    raise ValueError("MONGODB_URI is not available")