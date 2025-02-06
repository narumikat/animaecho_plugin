import asyncio
import websockets
import json
from pydub import AudioSegment
from pydub.playback import play
import threading
from io import BytesIO
import numpy as np


VTUBE_STUDIO_URL = "ws://localhost:8001/"
TOKEN_FILE = "vtube_studio_token.json"


def calculate_intensity(audio):
    samples = np.array(audio.get_array_of_samples())
    return np.abs(samples).mean() / np.iinfo(samples.dtype).max


# async def authenticate_with_vtube_studio(websocket):
#     auth_payload = {
#         "apiName": "VTubeStudioPublicAPI",
#         "apiVersion": "1.0",
#         "requestID": "auth_request_001",
#         "messageType": "AuthenticationRequest",
#         "data": {
#             "pluginName": "AnimaEcho",
#             "pluginDeveloper": "Narumi Katayama",
#             "authenticationToken": None
#         }
#     }
#     await websocket.send(json.dumps(auth_payload))
#     response = await websocket.recv()
#     print("Authentication in VTube Studio:", response)

def save_auth_token(token):
    with open(TOKEN_FILE, "w") as token_file:
        json.dump({"auth_token": token}, token_file)


def load_auth_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as token_file:
            return json.load(token_file).get("auth_token")
    return None

async def authenticate_with_vtube_studio(websocket):
    auth_token = load_auth_token()
    if not auth_token:
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


async def play_audio_with_lip_sync(audio):
    async with websockets.connect(VTUBE_STUDIO_URL) as websocket:
        await authenticate_with_vtube_studio(websocket)
        audio_thread = threading.Thread(target=lambda: play(audio))
        audio_thread.start()
        await send_lip_sync(websocket, audio)
        audio_thread.join()
