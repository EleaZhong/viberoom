# Echo Vibe Room

## Overview
This project is a sentiment analysis application that records audio, transcribes it, performs sentiment analysis on the transcriptions, and visualizes the sentiment data. It consists of three main components:

1. A server that receives and stores sentiment data.
2. A sensor client that records audio, transcribes it, performs sentiment analysis, and sends the sentiment data to the server.
3. A display client that fetches the sentiment data from the server and visualizes it.

## Setup and Run

1. Install the required packages:
```bash
pip install fastapi uvicorn python-dotenv google-cloud-speech google-cloud-language matplotlib pyaudio wave requests openai
```
2. Create a `.env` file in the root directory and add your OpenAI API key:
```bash
echo "OPENAI_API_KEY=your_api_key" > .env
```
3. Run the server:
```bash
uvicorn server:app --reload
```
4. In a new terminal, run the sensor client:
```bash
python client.py
```
5. In another new terminal, run the display client:
```bash
python3 -m http.server 8001
```
6. Open your web browser and navigate to:
```bash
http://localhost:8001/index.html
```

## Code Overview


The server is implemented in server.py and uses FastAPI to create a REST API that receives and stores sentiment data.

The sensor client is implemented in client.py. It records audio, transcribes it using the OpenAI API, performs sentiment analysis using the Google Cloud Language API, and sends the sentiment data to the server.

The display client is a p5.js sketch implemented in display.js. It fetches the sentiment data from the server and visualizes it.

The .gitignore file is used to ignore files and directories that should not be tracked by Git.



## Note



The recordings/, notes/, and logs/ directories are used by the sensor client to store audio recordings, transcriptions, and logs, respectively. These directories are ignored by Git as specified in the .gitignore file.