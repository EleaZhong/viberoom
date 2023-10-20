
import os
import io
import requests
import pyaudio
import wave
from google.cloud import speech
from google.cloud import language_v2
from matplotlib import pyplot as plt
from queue import Queue
import logging
from dotenv import load_dotenv
import threading
import openai


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def set_up():
    os.makedirs("logs", exist_ok=True)
    os.makedirs("recordings", exist_ok=True)
    os.makedirs("notes", exist_ok=True)


def setup_recording_logger():
    recording_logger = logging.getLogger("recording")
    recording_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("logs/record.log")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
    file_handler.setFormatter(formatter)
    recording_logger.addHandler(file_handler)
    return recording_logger


def setup_processing_logger():
    processing_logger = logging.getLogger("processing")
    processing_logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("logs/process.log")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
    file_handler.setFormatter(formatter)
    processing_logger.addHandler(file_handler)
    return processing_logger


def record_audio(filename):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    RECORD_SECONDS = 3

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    recording_logger.info("Recording...")
    frames = []
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    recording_logger.info("Finished recording")
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(filename, "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()


def continuous_recording(queue):
    recording_number = 0  # Make sure this starts as an integer
    last_filename = None
    
    while True:
        # Convert recording_number to int to make sure the formatting works
        recording_number = int(recording_number)
        
        filename = f"recordings/recording-{recording_number:04d}.wav"
        record_audio(filename)
        recording_logger.info("Filename: " + str(filename))
        
        if last_filename:
            combined_filename = f"recordings/combined-{recording_number:04d}.wav"
            
            with wave.open(combined_filename, 'wb') as outfile:
                # Open first file to read its headers
                with wave.open(last_filename, 'rb') as infile:
                    params = infile.getparams()
                    outfile.setparams(params)
                
                # Now proceed to read frames from each file and write
                for fname in [last_filename, filename]:
                    with wave.open(fname, 'rb') as infile:
                        outfile.writeframes(infile.readframes(infile.getnframes()))
            
            queue.put(combined_filename)
            recording_logger.info("Combined Filename: " + str(combined_filename))
        else:
            queue.put(filename)
        
        last_filename = filename
        recording_number += 1


def transcribe_audio(filename):
    with open(filename, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
    return transcript["text"]


def analyze_sentiment(text_content: str = "I am so happy and joyful.") -> [float, float]:
    """
    Analyzes Sentiment in a string.

    Args:
      text_content: The text content to analyze.
    """

    client = language_v2.LanguageServiceClient()

    # text_content = 'I am so happy and joyful.'

    # Available types: PLAIN_TEXT, HTML
    document_type_in_plain_text = language_v2.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language_code = "en"
    document = {
        "content": text_content,
        "type_": document_type_in_plain_text,
        "language_code": language_code,
    }

    # Available values: NONE, UTF8, UTF16, UTF32
    # See https://cloud.google.com/natural-language/docs/reference/rest/v2/EncodingType.
    encoding_type = language_v2.EncodingType.UTF8

    response = client.analyze_sentiment(
        request={"document": document, "encoding_type": encoding_type}
    )
    # Get overall sentiment of the input document
    print(f"Document sentiment score: {response.document_sentiment.score}")
    print(f"Document sentiment magnitude: {response.document_sentiment.magnitude}")
    # Get sentiment for all sentences in the document
    sentiments = []
    magnitudes = []
    for sentence in response.sentences:
        print(f"Sentence text: {sentence.text.content}")
        print(f"Sentence sentiment score: {sentence.sentiment.score}")
        print(f"Sentence sentiment magnitude: {sentence.sentiment.magnitude}")
        sentiments.append(sentence.sentiment.score)
        magnitudes.append(sentence.sentiment.magnitude)

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
    print(f"Language of the text: {response.language_code}")
    return response.document_sentiment.score, response.document_sentiment.magnitude, sentiments, magnitudes

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

def process_audio(queue):
    while True:
        filename = queue.get()
        transcript = transcribe_audio(filename)
        document_score, document_magnitude, sentiments, magnitudes = analyze_sentiment(transcript)
        processing_logger.info("Filename: " + str(filename))
        processing_logger.info("Transcript: " + str(transcript))
        processing_logger.info("Document Score: " + str(document_score))
        processing_logger.info("Document Magnitude: " + str(document_magnitude))
        processing_logger.info("Sentiments: " + str(sentiments))
        processing_logger.info("Magnitudes: " + str(magnitudes))
        status_code = send_to_server(document_score, document_magnitude)
        if status_code == 200:
            processing_logger.info('Sentiment analysis data sent to server successfully.')
        else:
            processing_logger.info('Failed to send sentiment analysis data to server.')


def main():

    recording_queue = Queue()

    recording_thread = threading.Thread(
        target=continuous_recording, args=(recording_queue,))
    recording_thread.start()

    processing_thread = threading.Thread(
        target=process_audio, args=(recording_queue,))
    processing_thread.start()

if __name__ == '__main__':
    set_up()
    recording_logger = setup_recording_logger()
    processing_logger = setup_processing_logger()
    main()
