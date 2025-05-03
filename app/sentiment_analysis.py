from ibm_watson import NaturalLanguageUnderstandingV1 # type: ignore
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions # type: ignore
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator # type: ignore

authenticator = IAMAuthenticator('YOUR_API_KEY_HERE')
nlu = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
)
nlu.set_service_url('YOUR_URL_HERE')

def analyze_sentiment(text):
    response = nlu.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()
    return response['sentiment']['document']['label']
