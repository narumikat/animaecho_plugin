import asyncio
import base64

import websockets
import json
import os
from pydub import AudioSegment
from pydub.playback import play
import threading
from io import BytesIO
import numpy as np

VTUBE_STUDIO_URL = "ws://localhost:8001/"
TOKEN_FILE = "vtube_studio_token.json"

def save_auth_token(token):
    print("💾 Saving authentication token to local file...")
    with open(TOKEN_FILE, "w") as token_file:
        json.dump({"auth_token": token}, token_file)


def calculate_intensity(audio):
    samples = np.array(audio.get_array_of_samples())
    return np.abs(samples).mean() / np.iinfo(samples.dtype).max


def decode_and_convert_audio(audio_base64):
    audio_data = base64.b64decode(audio_base64)
    return AudioSegment.from_file(BytesIO(audio_data))


def load_auth_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file).get("auth_token")
    return None


async def authenticate_with_vtube_studio(websocket):
    print("🔑 Starting authentication with VTube Studio...")
    auth_token = load_auth_token()

    if not auth_token:
        print("🔓 Requesting new authentication token...")
        print("⚠️ **IMPORTANT:** Accept the permission within VTube Studio!")
        print("📢 **Go to VTube Studio settings and accept the 'AnimaEcho' plugin.**")

        token_request_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "token_request_001",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "AnimaEcho",
                "pluginDeveloper": "Narumi Katayama"
            }
        }
        await websocket.send(json.dumps(token_request_payload))
        token_response = await websocket.recv()
        token_data = json.loads(token_response)
        auth_token = token_data["data"]["authenticationToken"]
        save_auth_token(auth_token)
    auth_request_payload = {
        "apiName": "VTubeStudioPublicAPI",
        "apiVersion": "1.0",
        "requestID": "auth_request_001",
        "messageType": "AuthenticationRequest",
        "data": {
            "pluginName": "AnimaEcho",
            "pluginDeveloper": "Narumi Katayama",
            "authenticationToken": auth_token
        }
    }
    await websocket.send(json.dumps(auth_request_payload))
    await websocket.recv()


async def send_lip_sync(websocket, audio, chunk_duration=100, stop_before=0.8):
    total_duration = len(audio)
    stop_time = total_duration - (stop_before * 1000)
    chunks = audio[::chunk_duration]
    for start_time, chunk in enumerate(chunks):
        current_time = start_time * chunk_duration
        if current_time >= stop_time:
            break
        intensity = calculate_intensity(chunk)
        mouth_open_value = min(intensity * 2, 1.0)
        mouth_smile_value = min(intensity * 0.5, 1.0)

        lip_sync_payload = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "lip_sync_001",
            "messageType": "InjectParameterDataRequest",
            "data": {
                "parameterValues": [
                    {"id": "MouthOpen", "value": mouth_open_value},
                    {"id": "MouthSmile", "value": mouth_smile_value}
                ]
            }
        }
        await websocket.send(json.dumps(lip_sync_payload))
        await websocket.recv()
        await asyncio.sleep(chunk_duration / 1000)


async def play_audio_with_lip_sync(audio_input):
    if isinstance(audio_input, str):
        audio = decode_and_convert_audio(audio_input)
    elif isinstance(audio_input, AudioSegment):
        audio = audio_input
    else:
        raise TypeError("Invalid audio input. Must be Base64 string or AudioSegment.")

    print("🌐 Connecting to VTube Studio WebSocket...")
    async with websockets.connect(VTUBE_STUDIO_URL) as websocket:
        await authenticate_with_vtube_studio(websocket)
        print("🔊 Playing audio...")
        audio_thread = threading.Thread(target=lambda: play(audio))
        audio_thread.start()
        await send_lip_sync(websocket, audio)
        audio_thread.join()

        print("✅ Audio playback and Lip Sync completed.")
