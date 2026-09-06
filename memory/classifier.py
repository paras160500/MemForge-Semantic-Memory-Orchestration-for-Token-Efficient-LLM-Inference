#============================================================================
#                             Import Statments
#============================================================================

from llm.client import OpenAIClient
from llm.prompts import CLASSIFICATION_SYSTEM_PROMPT

#============================================================================
#                             Classifier Statments
#============================================================================

class InputClassfier:

    def __init__(self):
        self.llm = OpenAIClient()

    def classify(self , user_input : str):
        response = self.llm.chat(
            [
                {
                    "role" : "system",
                    "content" : CLASSIFICATION_SYSTEM_PROMPT
                },
                {
                    "role" : "user",
                    "content" : user_input
                }
            ],
            temperature=0
        )

        result = response['content'].strip().lower()

        if result == "query":
            return "query"
        if result == "statement":
            return "statement"

        # Fallback
        if user_input.strip().endswith("?"):
            return "query"

        return "statement"