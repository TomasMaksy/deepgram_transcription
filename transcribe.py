import asyncio
import os
import sounddevice as sd
import numpy as np
from deepgram import Deepgram


DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')
DEEPGRAM_API_URL = 'wss://api.deepgram.com/v1/listen?model=nova-2&language=lt'

# Create a Deepgram client
deepgram = Deepgram(DEEPGRAM_API_KEY)

# Audio parameters
SAMPLE_RATE = 16000  # Deepgram recommends 16kHz for audio
CHANNELS = 1  # Mono audio
BLOCK_SIZE = 1024  # Number of samples per block

async def transcribe_audio():
    # Connect to the Deepgram WebSocket
    async with deepgram.transcription.live({'punctuate': True}) as socket:
        # Callback function to send audio data
        def callback(indata, frames, time, status):
            if status:
                print(status)
            # Convert audio data to bytes and send to Deepgram
            socket.send(indata.tobytes())
            
        # Start streaming audio from the microphone
        with sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, blocksize=BLOCK_SIZE, callback=callback):
            print("Listening...")
            while True:
                # Wait for transcription results
                response = await socket.recv()
                if 'channel' in response:
                    transcript = response['channel']['alternatives'][0]['transcript']
                    print(f'Transcription: {transcript}')

# Run the transcription function
if __name__ == "__main__":
    asyncio.run(transcribe_audio())