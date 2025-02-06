import requests
from pydub import AudioSegment
from pydub.playback import play
from animaecho_plugin.audio_processing import record_audio_as_blob
from animaecho_plugin.vtube_studio import play_audio_with_lip_sync
import asyncio
from io import BytesIO

# URL do endpoint da API principal
API_ENDPOINT = "https://8441-2400-2411-3923-7000-5c97-fc8c-2bb3-9ece.ngrok-free.app/api/process_audio/"


def send_audio_to_server(audio_blob):
    try:
        print("Sending audio to the main API...")
        files = {'audio': ('audio.wav', audio_blob, 'audio/wav')}
        response = requests.post(API_ENDPOINT, files=files)

        if response.status_code == 200:
            print("✅ Audio processed successfully.")
            return AudioSegment.from_file(BytesIO(response.content), format="wav")
        else:
            print(f"❌ Error processing audio on server: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error sending audio: {str(e)}")
        return None


def main():
    try:
        print("🎙️ Recording audio...")
        audio_blob = record_audio_as_blob(duration=5)
        print("✅ Recording completed.")

        processed_audio = send_audio_to_server(audio_blob)

        if processed_audio:
            print("Starting sync with VTube Studio...")
            audio = AudioSegment.from_file(processed_audio)
            asyncio.run(play_audio_with_lip_sync(audio))
            print("✅ Synchronization completed.")
        else:
            print("❌ Failed to process audio.")

    except Exception as e:
        print(f"❌ Plugin error: {str(e)}")


# def main():
#     try:
#         print("🎙️ Recording audio...")
#         audio_blob = record_audio_as_blob(duration=5)
#         print("✅ Recording completed.")
#
#         processed_audio = send_audio_to_server(audio_blob)
#
#         if processed_audio:
#             print("Starting sync with VTube Studio...")
#             asyncio.run(play_audio_with_lip_sync(processed_audio))
#             print("✅ Synchronization completed.")
#         else:
#             print("❌ Failed to process audio.")
#
#     except Exception as e:
#         print(f"❌ Plugin error: {str(e)}")


if __name__ == "__main__":
    main()
