from django.http import StreamingHttpResponse
from openai import OpenAI
from django.conf import settings


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

        prompt = (
            f"You are a creative gift suggestion assistant. Generate 5-10 unique, thoughtful, "
            f"and practical gift ideas based on the following parameters:\n"
            f"- Age: {age}\n"
            f"- Gender: {gender}\n"
            f"- Budget: {budget}\n"
            f"- Interests: {interests}\n"
            f"- Relationship with the gift receiver: {relationship}\n\n"
            "Ensure the gift ideas are:\n"
            "1. Within the budget range.\n"
            "2. Relevant to the age and gender.\n"
            "3. Aligned with the interests, if provided.\n"
            "4. Appropriate for the relationship context (e.g., friend, parent, spouse).\n\n"
            "Format the response as a json list of objects with a short description for each gift."
        )

        def stream_response():
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system",
                     "content": "You are a helpful assistant for generating personalized gift ideas."},
                    {"role": "user", "content": prompt},
                ],
                response_format={"type": "json_object"},
                temperature=0.5,
                stream=True
            )
            for chunk in response:
                yield chunk.choices[0].delta.content

        return StreamingHttpResponse(stream_response(), content_type="application/json")
