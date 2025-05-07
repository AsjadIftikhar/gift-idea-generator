from django.http import StreamingHttpResponse
from openai import OpenAI
from django.conf import settings
import threading
import queue


class DeepSeekService:
    def __init__(self):
        self.api_key = settings.API_KEY
        self.base_url = settings.BASE_URL
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def generate_gift_ideas(self, params):
        age = params.get("age", "unknown age")
        gender = params.get("gender", "unknown gender")
        budget = params.get("budget", "unknown budget")
        interests = params.get("interests", "no specific interests")
        relationship = params.get("relationship", "no specific relationship")

        # Simplified prompt with fewer tokens
        prompt = (
            f"Generate 5 gift ideas for {age} {gender}, budget: {budget}, "
            f"interests: {interests}, relationship: {relationship}."
        )

        def stream_response():
            response_queue = queue.Queue()
            
            def fetch_response():
                response = self.client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system",
                         "content": "You are a gift suggestion assistant. Provide concise gift ideas in JSON format with a list of objects containing 'name' and 'description' fields."},
                        {"role": "user", "content": prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.2,
                    stream=True
                )
                for chunk in response:
                    if hasattr(chunk.choices[0].delta, 'content') and chunk.choices[0].delta.content is not None:
                        response_queue.put(chunk.choices[0].delta.content)
                response_queue.put(None)  # Signal completion
            
            # Start API call in a separate thread
            thread = threading.Thread(target=fetch_response)
            thread.daemon = True
            thread.start()
            
            # Yield results as they become available
            while True:
                chunk = response_queue.get()
                if chunk is None:
                    break
                yield chunk

        return StreamingHttpResponse(stream_response(), content_type="application/json")
