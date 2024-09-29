import sys
import time
import obswebsocket
from obswebsocket import obsws, requests

def update_subtitle(queue):
    # Set your OBS connection settings
    host = "192.168.0.117"
    port = 4455  # default OBS WebSocket port
    password = "yanR4ukg8UGGv2PR"  # Set your OBS WebSocket password here if you have one

    # Start the OBS WebSocket connection
    ws = obsws(host, port, password)
    ws.connect()

    source_name = 'transcribe'  # Ensure this matches your OBS text source name

    print("Waiting for subtitles...")
    while True:
        try:
            if not queue.empty():
                # Get the latest subtitle from the queue
                subtitle = queue.get()

                # Send the subtitle to OBS
                ws.call(requests.SetInputSettings(
                    inputName=source_name,
                    inputSettings={"text": subtitle}
                ))
                print(f"Updated subtitle: {subtitle}")

            # Sleep for a short time before checking the queue again
            time.sleep(0.5)  # Adjust this as needed

        except Exception as e:
            print(f"Error updating subtitle: {e}")

    # Remember to close the OBS WebSocket connection when done
    ws.disconnect()
