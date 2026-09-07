#============================================================================
#                             Import Statments
#============================================================================
from openai import OpenAI
from config.settings import (
    OPENAI_API_KEY,
    OPENAI_CHAT_MODEL,
)

#============================================================================
#                               Class Statments
#============================================================================
class OpenAIClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY,timeout=60.0)
        self.model = OPENAI_CHAT_MODEL

    def chat(self , messages , temperature = 0):
        response = self.client.chat.completions.create(model=self.model , messages=messages)
        message = response.choices[0].message
        usage = response.usage
        prompt_tokens = (getattr(usage , "prompt_tokens" , 0) if usage else 0)
        completion_tokens = (getattr(usage , "completion_tokens" , 0) if usage else 0)
        return {
            "content" : message.content,
            "prompt_tokens" : prompt_tokens,
            "completion_tokens" : completion_tokens,
            "total_tokens" : prompt_tokens + completion_tokens
        }

    