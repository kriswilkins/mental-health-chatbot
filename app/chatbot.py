from chatterbot import ChatBot
from ibm_watson import NaturalLanguageUnderstandingV1 # type: ignore
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions # type: ignore
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator # type: ignore
import asyncio
import aiohttp # type: ignore
from cachetools import TTLCache # type: ignore

chatbot = ChatBot(
    'TherapistBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='sqlite:///database.sqlite3'
)

authenticator = IAMAuthenticator('YOUR_API_KEY_HERE')
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url('YOUR_URL_HERE')

cache = TTLCache(maxsize=100, ttl=300)

import httpx # type: ignore
import asyncio

cache = {}

async def get_chatbot_response(user_input):
    if user_input in cache:
        return cache[user_input]

    # Ensure the input text meets the minimum length requirement
    min_length = 20  # Adjust this value as needed
    if len(user_input) < min_length:
        additional_text = " This is additional text to meet the minimum length requirement."
        user_input += additional_text[:min_length - len(user_input)]

    features = {
        'sentiment': {}
    }

    payload = {
        'text': user_input,
        'features': features
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=f'{nlu.service_url}/v1/analyze?version=2021-08-01',
                headers={
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {nlu.authenticator.token_manager.get_token()}'
                },
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            response_data = response.json()

    except httpx.HTTPStatusError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.content}")
        raise
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        raise

    sentiment = response_data['sentiment']['document']['label']
    
    chatbot_response = chatbot.get_response(user_input)
    
    cache[user_input] = (str(chatbot_response), sentiment)
    
    return str(chatbot_response), sentiment
