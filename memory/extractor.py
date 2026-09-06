#============================================================================
#                             Import Statments
#============================================================================

import json
from llm.client import OpenAIClient
from llm.prompts import FACT_EXTRACTION_SYSTEM_PROMPT, build_fact_extraction_prompt

#============================================================================
#                              Extractor Statments
#============================================================================

class FactExtractor:

    def __init__(self):
        self.llm = OpenAIClient()

    @staticmethod
    def _parse_response(response_text : str):
        try:
            start = response_text.find("[")
            end = response_text.rfind("]")

            if(start == -1 or end == -1 or end < start):
                return []

            json_text = response_text[start : end + 1]
            data = json.loads(json_text)

            if not isinstance(data , list):
                return []
            facts = []

            for item in data:
                if isinstance(item , str):
                    cleaned = item.strip()
                    if cleaned:
                        facts.append(cleaned)

            return facts
        except(json.JSONDecodeError , TypeError):
            return []    


    def extract_facts(self , statement : str , recent_context : str = ""):
        prompt = (
            build_fact_extraction_prompt(statement=statement , recent_context=recent_context)
        )
        response = (
            self.llm.chat(
                [
                    {
                        "role" : "system" , "content" : FACT_EXTRACTION_SYSTEM_PROMPT
                    },
                    {
                        "role" : "user" , "content" : prompt
                    }
                ],
                temperature=0
            )
        )

        return self._parse_response(response['content'])

    