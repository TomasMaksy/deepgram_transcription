import multiprocessing
from transcribe import transcribe  
from subtitle_generation import update_subtitle 

if __name__ == "__main__":
    # Create a Queue for inter-process communication
    transcription_queue = multiprocessing.Queue()

    # Start the transcription process
    transcribe_process = multiprocessing.Process(target=transcribe, args=(transcription_queue,))
    transcribe_process.start()

    # Start the subtitle update process
    # Adjust the import of ws as necessary in subtitle_generation.py
    # You can create a function that accepts the ws parameter and the queue
    update_subtitle_process = multiprocessing.Process(target=update_subtitle, args=(transcription_queue,))
    update_subtitle_process.start()

    # Keep the main process alive
    transcribe_process.join()
    update_subtitle_process.join()
