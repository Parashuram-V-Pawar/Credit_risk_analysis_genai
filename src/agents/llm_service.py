from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class LLMService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("API_KEY")
        )

        self.model = "llama-3.3-70b-versatile"

    def generate(self, prompt: str):

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content