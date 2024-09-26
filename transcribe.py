# Coded by maksy
# Tomas Maksimovic use for Klub u Redaktorow by Wilnoteka
##################################################################

from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from time import sleep

import multiprocessing

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()


def transcribe(queue):
    try:
        deepgram = DeepgramClient()
        dg_connection = deepgram.listen.websocket.v("1")

        def on_open(self, open, **kwargs):
            print(f"\n{open}\n")

        def on_message(self, result, **kwargs):
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) == 0:
                return
            #print(f"{sentence}")
            
            # Push the transcription to the queue
            queue.put(sentence)
            # print(f"Queud: {sentence}") # - troubleshooting


        def on_unhandled(self, unhandled, **kwargs):
            print(f"\n\n{unhandled}\n\n")


        dg_connection.on(LiveTranscriptionEvents.Open, on_open)
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
        dg_connection.on(LiveTranscriptionEvents.Unhandled, on_unhandled)

        options = {
            "model": "nova-2",
            "punctuate": True,
            "language": "pl",
            "encoding": "linear16",
            "channels": 1,
            "sample_rate": 16000,
            "vad_events": True,
        }

        if dg_connection.start(options) is False:
            print("Failed to connect to Deepgram")
            return

        print("\n\nPress Enter to stop recording...\n\n")



        microphone = Microphone(dg_connection.send)
        microphone.start()
        while True: 
            try:
                input("")  # Wait for user input
                break  # Exit the loop on Enter key
            except EOFError:
                pass  # Ignore EOFError and continue waiting for input
        microphone.finish()
        dg_connection.finish()
        print("Finished")

    except Exception as e:
        print(f"Could not open socket: {e}")
        return

if __name__ == "__main__":
    # Create a Queue for inter-process communication
    transcription_queue = multiprocessing.Queue()

    # Start the transcription process
    transcribe_process = multiprocessing.Process(target=transcribe, args=(transcription_queue,))
    transcribe_process.start()

    # Keep the main process alive
    transcribe_process.join()
