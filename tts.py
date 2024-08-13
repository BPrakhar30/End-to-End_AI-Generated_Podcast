import os
from pathlib import Path
from openai import OpenAI
from pydub import AudioSegment

def generate_tts_for_script(client, file_path, prepend_file_path, outro_file_path, output_dir):
    voices = {
        "Dan": "onyx",
        "Default": "fable"
    }

    # Ensuring the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Reading the script file
    with open(file_path, 'r', encoding="utf-8") as file:
        script_text = file.read()

    # Dividing the script into manageable parts
    parts = [script_text[i:i+4096] for i in range(0, len(script_text), 4096)]
    audio_segments = []

    # Generating TTS for each part using Dan's voice
    for part in parts:
        response = client.audio.speech.create(
            model="tts-1",
            voice=voices["Dan"],
            input=part,
            response_format='wav'
        )
        part_audio_path = Path(output_dir) / "part_audio.wav"
        with open(part_audio_path, 'wb') as audio_file:
            audio_file.write(response.content)
        part_audio = AudioSegment.from_file(part_audio_path)
        audio_segments.append(part_audio)
        os.remove(part_audio_path)  # Cleaning up the part file immediately after use

    # Loading the prepend audio file (intro)
    prepend_audio = AudioSegment.from_file(prepend_file_path)

    # Combining prepend audio with the script audio
    combined_audio = prepend_audio
    for segment in audio_segments:
        combined_audio += segment

    # Generating and add the closing statement
    closing_message = "This podcast is AI generated.........................."
    closing_response = client.audio.speech.create(
        model="tts-1",
        voice=voices["Default"],
        input=closing_message,
        response_format='wav'
    )
    closing_audio_path = Path(output_dir) / "closing_statement.wav"
    with open(closing_audio_path, 'wb') as closing_file:
        closing_file.write(closing_response.content)
    closing_audio = AudioSegment.from_file(closing_audio_path)

    # Appending the closing statement audio
    combined_audio += closing_audio

    # Loading the outro audio file
    outro_audio = AudioSegment.from_file(outro_file_path)
    combined_audio += outro_audio

    os.remove(closing_audio_path)  # Cleaning up the closing statement file

    # Saving the combined audio to a single file
    final_audio_path = Path(output_dir) / "episode.mp3"
    combined_audio.export(final_audio_path, format="mp3")

    print(f"Combined audio created at: {final_audio_path}")
