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

    def decide_operation(
        self,
        fact: str,
        similar_memories
    ):

        print(
            "Preparing memory decision..."
        )


        if not similar_memories:

            similar_memory_text = (
                "No similar memories found."
            )

        else:

            lines = []

            for index, (
                memory,
                score
            ) in enumerate(
                similar_memories,
                start=1
            ):

                lines.append(
                    f"""
    {index}.
    Memory ID: {memory.id}
    Similarity: {score:.4f}
    Text: {memory.text}
    """
                )

            similar_memory_text = (
                "\n".join(lines)
            )


        prompt = (
            build_memory_update_prompt(
                candidate_fact=fact,

                similar_memories=
                    similar_memory_text,
            )
        )


        print(
            "Sending memory decision to OpenAI..."
        )


        response = (
            self.llm.chat(
                [
                    {
                        "role": "system",
                        "content":
                            "Return only valid JSON.",
                    },

                    {
                        "role": "user",
                        "content":
                            prompt,
                    },
                ],

                temperature=0
            )
        )


        print(
            "OpenAI memory decision received."
        )


        return self._parse_json(
            response["content"]
        )
        

    # --------------------------------Process Fact--------------------------------
    def _process_fact(
        self,
        fact: str,
        turn_index: int
    ):

        print("\n" + "=" * 60)
        print("MEMORY UPDATE STARTED")
        print("=" * 60)

        print(f"FACT: {fact}")

        # --------------------------------------------------------
        # STEP 1 — EMBEDDING
        # --------------------------------------------------------

        print("\n[1/4] Creating embedding...")

        fact_embedding = (
            self.embeddings
            .get_embedding(fact)
        )

        print(
            f"[1/4] Embedding created successfully "
            f"({len(fact_embedding)} dimensions)"
        )


        # --------------------------------------------------------
        # STEP 2 — SEARCH SIMILAR MEMORIES
        # --------------------------------------------------------

        print(
            "\n[2/4] Searching similar memories..."
        )

        similar_memories = (
            self.memory_store
            .find_semantically_similar_memories(
                query_embedding=fact_embedding,

                top_k=
                    SIMILAR_MEMORIES_FOR_UPDATE,

                threshold=
                    MEMORY_SIMILARITY_THRESHOLD,
            )
        )

        print(
            f"[2/4] Found "
            f"{len(similar_memories)} "
            f"similar memories"
        )


        # --------------------------------------------------------
        # STEP 3 — ASK CHATGPT
        # --------------------------------------------------------

        print(
            "\n[3/4] Asking ChatGPT "
            "whether to ADD / UPDATE / NOOP..."
        )

        decision = (
            self.decide_operation(
                fact,
                similar_memories
            )
        )

        print(
            f"[3/4] ChatGPT decision: "
            f"{decision}"
        )


        operation = (
            decision
            .get(
                "operation",
                "NOOP"
            )
            .upper()
        )


        # --------------------------------------------------------
        # STEP 4 — APPLY DECISION
        # --------------------------------------------------------

        if operation == "ADD":

            print(
                "\n[4/4] Adding new memory..."
            )

            memory = MemoryItem(
                text=fact,

                embedding=
                    fact_embedding.tolist(),

                source_turn_indices=[
                    turn_index
                ],
            )

            self.memory_store.add_memory_item(
                memory
            )

            print(
                "[4/4] Memory added successfully"
            )

            print("=" * 60)

            return {
                "operation": "ADD",

                "memory_id": memory.id,

                "fact": fact,
            }


        if operation == "UPDATE":

            target_memory_id = (
                decision.get(
                    "target_memory_id"
                )
            )

            updated_memory_text = (
                decision.get(
                    "updated_memory_text"
                )
            )

            if (
                target_memory_id
                and updated_memory_text
            ):

                print(
                    "\n[4/4] Updating existing memory..."
                )

                updated_embedding = (
                    self.embeddings
                    .get_embedding(
                        updated_memory_text
                    )
                )

                success = (
                    self.memory_store
                    .update_existing_memory_item(
                        memory_id=
                            target_memory_id,

                        new_text=
                            updated_memory_text,

                        new_embedding=
                            updated_embedding,

                        turn_indices=[
                            turn_index
                        ],
                    )
                )

                if success:

                    print(
                        "[4/4] Memory updated successfully"
                    )

                    print("=" * 60)

                    return {
                        "operation":
                            "UPDATE",

                        "memory_id":
                            target_memory_id,

                        "fact":
                            updated_memory_text,
                    }


        print(
            "\n[4/4] No memory change required"
        )

        print("=" * 60)

        return {
            "operation": "NOOP",

            "fact": fact,
        }
    