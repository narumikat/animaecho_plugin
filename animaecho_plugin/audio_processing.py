import wave
from io import BytesIO
from pydub import AudioSegment

# Main API endpoint URL
API_ENDPOINT = "https://8441-2400-2411-3923-7000-5c97-fc8c-2bb3-9ece.ngrok-free.app/api/process_audio/"

def record_audio_as_blob(duration=5):
    import pyaudio

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    frames = [stream.read(CHUNK) for _ in range(0, int(RATE / CHUNK * duration))]
    stream.stop_stream()
    stream.close()
    p.terminate()
    audio_buffer = BytesIO()
    with wave.open(audio_buffer, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    audio_buffer.seek(0)
    return audio_buffer

def send_audio_to_server(audio_blob):
    import base64
    import requests

    try:
        print("🌐 Sending audio to the main API...")
        files = {'audio': ('audio.wav', audio_blob, 'audio/wav')}
        response = requests.post(API_ENDPOINT, files=files)

        if response.status_code == 200:
            print("✅ Audio processed successfully.")
            response_data = response.json()

            if "audio_file" in response_data:
                audio_bytes = base64.b64decode(response_data["audio_file"])

                audio = AudioSegment.from_file(BytesIO(audio_bytes))
                return audio
            else:
                print("❌ Audio file missing in API response.")
                return None
        else:
            print(f"❌ API returned an error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error sending audio: {str(e)}")
        return None