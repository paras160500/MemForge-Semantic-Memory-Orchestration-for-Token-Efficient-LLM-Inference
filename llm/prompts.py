CLASSIFICATION_SYSTEM_PROMPT = """
You are a classifier for a memory-enabled AI assistant.

Determine whether the user's input is a QUERY or a STATEMENT.

A QUERY:
- asks a question
- requests information
- asks the assistant to perform something

A STATEMENT:
- provides information
- expresses a preference
- describes a goal
- describes a plan
- gives a decision
- provides information that may be useful later

Return ONLY:
query
or
statement
"""


FACT_EXTRACTION_SYSTEM_PROMPT = """
        You are an expert long-term memory extraction system.

        Your job is to extract useful facts from a user's statement.

        Extract only information that could be useful in future
        conversations.

        Focus on:

        - preferences
        - goals
        - plans
        - decisions
        - important entities
        - important values
        - user-provided facts

        Do NOT invent information.

        Do NOT make assumptions.

        Do NOT include questions.

        Do NOT include conversational filler.

        Return ONLY a valid JSON array of strings.

        Example:

        [
            "The user's target audience is young adults aged 18-25.",
            "The campaign budget is $5000."
        ]

        If there is no useful information:

        []
"""

def build_fact_extraction_prompt(statement : str , recent_context : str):
    return f"""
        Extract useful long-term facts from the following
        user statement.

        Recent conversation context:

        --- BEGIN CONTEXT ---

        {recent_context}

        --- END CONTEXT ---

        New user statement:

        "{statement}"

        Return ONLY a JSON array of concise declarative facts.
    """

def build_memory_update_prompt(candidate_fact : str , similar_memories : str):
    return f"""
        You are managing a long-term semantic memory system.
        A new fact has been extracted:
        "{candidate_fact}"
        The following memories are semantically similar:
        {similar_memories}
        Choose exactly one operation:

        ADD
        UPDATE
        NOOP

        ADD:
        The information is new and should be stored.

        UPDATE:
        The new information changes, replaces, or improves
        an existing memory.

        NOOP:
        The information is already represented by an existing
        memory and does not provide meaningful new information.

        If you select UPDATE, return the target memory ID and
        the complete updated memory text.

        Return ONLY valid JSON.

        ADD example:

        {{
            "operation": "ADD"
        }}

        UPDATE example:

        {{
            "operation": "UPDATE",
            "target_memory_id": "memory-id",
            "updated_memory_text": "Updated memory text"
        }}

        NOOP example:

        {{
            "operation": "NOOP"
        }}
    """


def build_answer_prompt(
    query: str,
    relevant_memories: str
):

    return f"""
        You are a helpful AI assistant with long-term memory.

        Answer the user's question using relevant memories when
        they are available.

        Relevant memories:

        --- BEGIN MEMORY ---

        {relevant_memories}

        --- END MEMORY ---

        User question:

        "{query}"

        Rules:

        - Use relevant memory when appropriate.
        - Do not invent personal information.
        - Do not mention the memory system unless necessary.
        - Answer naturally and clearly.
    """