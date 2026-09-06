#============================================================================
#                                Import Statments
#============================================================================
import uuid
from datetime import datetime
from typing import List,Optional

#============================================================================
#                                Class Statments
#============================================================================
class MemoryItem:
    def __init__(
        self,text: str,embedding: Optional[List[float]] = None,
        source_turn_indices: Optional[List[int]] = None,
        memory_id: Optional[str] = None,
        creation_timestamp: Optional[datetime] = None,
        last_accessed_timestamp: Optional[datetime] = None,
        access_count: int = 0,
    ):

        self.id = (memory_id or str(uuid.uuid4()))
        self.text = text
        self.embedding = embedding
        self.creation_timestamp = (creation_timestamp or datetime.utcnow())
        self.last_accessed_timestamp = (last_accessed_timestamp or self.creation_timestamp)
        self.access_count = access_count
        self.source_turn_indices = (source_turn_indices or [])


    def mark_accessed(self):
        self.last_accessed_timestamp = (datetime.utcnow())
        self.access_count += 1


    def to_dict(self):
        return {
            "memory_id": self.id,
            "text": self.text,
            "embedding": self.embedding,
            "creation_timestamp":self.creation_timestamp,
            "last_accessed_timestamp":self.last_accessed_timestamp,
            "access_count":self.access_count,
            "source_turn_indices":self.source_turn_indices,
        }


    @classmethod
    def from_dict(cls,data):
        return cls(
            text=data["text"],
            embedding=data.get("embedding"),
            source_turn_indices=data.get("source_turn_indices",[]),
            memory_id=data.get("memory_id"),
            creation_timestamp=data.get("creation_timestamp"),
            last_accessed_timestamp=data.get("last_accessed_timestamp"),
            access_count=data.get("access_count",0),
        )

    def __repr__(self):
        return (
            f"MemoryItem("
            f"id={self.id}, "
            f"text='{self.text}', "
            f"access_count={self.access_count}"
            f")"
        )