
import os
import io
import requests
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.cloud import language_v1
from google.cloud.language_v1 import enums as language_enums

# Set up Google Cloud Speech and Language API clients
speech_client = speech.SpeechClient()
language_client = language_v1.LanguageServiceClient()

# Set up audio recording parameters
audio_format = enums.RecognitionConfig.AudioEncoding.LINEAR16
sample_rate_hertz = 16000
language_code = 'en-US'

def transcribe_audio(audio_file_path):
    """
    Transcribe the audio file using Google Cloud Speech API
    """
    with io.open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=audio_format,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code)

    response = speech_client.recognize(config, audio)

    # Get the transcription of the audio
    for result in response.results:
        return result.alternatives[0].transcript

def analyze_sentiment(text):
    """
    Analyze the sentiment of the text using Google Cloud Natural Language API
    """
    document = language_v1.Document(content=text, type_=language_enums.Document.Type.PLAIN_TEXT)
    sentiment = language_client.analyze_sentiment(request={'document': document}).document_sentiment

    return sentiment.score, sentiment.magnitude

def send_to_server(sentiment_score, sentiment_magnitude):
    """
    Send the sentiment analysis data to the server
    """
    data = {
        'sentiment_score': sentiment_score,
        'sentiment_magnitude': sentiment_magnitude
    }
    response = requests.post('http://localhost:8000/api/v1/sentiment', json=data)

    return response.status_code

def main():
    audio_file_path = 'audio.wav'  # Replace with the path to your audio file
    text = transcribe_audio(audio_file_path)
    sentiment_score, sentiment_magnitude = analyze_sentiment(text)
    status_code = send_to_server(sentiment_score, sentiment_magnitude)

    if status_code == 200:
        print('Sentiment analysis data sent to server successfully.')
    else:
        print('Failed to send sentiment analysis data to server.')

if __name__ == '__main__':
    main()

