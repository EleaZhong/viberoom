from dotenv import load_dotenv
import os
import requests
import random
import time

load_dotenv()

SPOTIFY_PLAYBACK_URL = 'https://api.spotify.com/v1/me/player/play'
ACCESS_TOKEN = "BQCCmN77MU_2L6eUXcE8zWItI33I356CeNHVu2G0uMSW_Ayph7KBfjWroBOaJkNsxA8JnmrGIZGncHKP-b8CxvLsNOts0ypL6Iy3u1SOxsceO8HfuNXkBiBnGQDCjH-RxWFS3zCZYko95wlKF5gEZ1iozWR3_sSNuHkeg0QHnMEu9JVxVb2trNOiUeZjE0o-Ae5lVY4"
#USE access_code.py: open returned URL, copy code in browser - after '/#access_token=', before '&token'


client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


def play_song(playlist_uri,song_pos):
     global ACCESS_TOKEN
     response = requests.put(
          SPOTIFY_PLAYBACK_URL,
          headers={
               "Authorization": f"Bearer {ACCESS_TOKEN}",
               "Content-Type": "application/json"
          },
          json={
              "context_uri": playlist_uri,
              "offset": {
                  "position": song_pos
              },
              "position_ms": 0
          }
     )
     print(response.content)
     #IF RETURNED 404 : NO_ACTIVE_DEVICE, restart IDE and Spotify desktop app, or restart PC
     return response


def excited_music():
    play_song(

    )


def neutral_music():
    play_song(
        playlist_uri="spotify:playlist:37i9dQZF1DXd2whofuA2Kb",
        song_pos=random.randrange(75)
    )


def happy_music():
    play_song(
        #replace playlist ID (in URL between 'playlist/' and '?si')
        playlist_uri="spotify:playlist:16YfgEGfLNu64hlQJwQQmS",
        # random index for song position - replace int with num of last song in playlist
        song_pos=random.randrange(17)
    )


def sad_music():
    play_song(
        # replace playlist ID (in URL between 'playlist/' and '?si')
        playlist_uri="spotify:playlist:37i9dQZF1DWWIvMGe3ig7a",
        # random index for song position - replace int with num of last song in playlist
        song_pos=random.randrange(35)
    )


def anger_music():
    play_song(
        # replace playlist ID (in URL between 'playlist/' and '?si')
        playlist_uri="spotify:playlist:37i9dQZF1EIe3mfu57ntxN",
        # random index for song position - replace int with num of last song in playlist
        song_pos=random.randrange(50)
    )

def surprise_music():
    play_song(
        #Pink Panther theme
        playlist_uri="spotify:album:4d1o8H5QwEsE6vdxOlC5e3",
        song_pos=21
    )

def change_song(pastvibe, vibe):
    if (pastvibe != vibe):
        print("Playing new song...")

        if (vibe == 'neutral' or vibe == ''):
            neutral_music()
        elif (vibe == 'happy'):
            happy_music()
        elif (vibe == 'excited'):
            excited_music()
        elif (vibe == 'sad'):
            sad_music()
        elif (vibe == 'anger'):
            anger_music()
        elif (vibe == 'surprise'):
            surprise_music()


def main():
    #CUT AND PASTE THIS SO THAT AN OLD AND NEW VIBE IS SENT TO CHANGE_SONG FUNC EVERY 30 SECONDS
    while True:
        print("Reading vibe...")

        change_song("happy","anger")
        time.sleep(30 - time.time() % 30)
    #PLEASE MOVE ABOVE CODE SNIPPET

if __name__ == '__main__':
     main()