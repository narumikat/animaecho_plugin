from animaecho_plugin.audio_processing import *
from animaecho_plugin.vtube_studio import play_audio_with_lip_sync
import asyncio


def main():
    try:
        print("🎙️ Recording audio for 5 seconds...")
        audio_blob = record_audio_as_blob(duration=5)
        print("✅ Recording completed.")

        processed_audio = send_audio_to_server(audio_blob)

        if processed_audio:
            # print(f"🔊 Audio type: {type(processed_audio)}")

            if isinstance(processed_audio, AudioSegment):
                print("✅ Proceeding with lip sync on VTubeStudio...")
                asyncio.run(play_audio_with_lip_sync(processed_audio))
                print("✅ Synchronization completed.")
            else:
                print(f"❌ Unexpected audio format: {type(processed_audio)}")
        else:
            print("❌ Failed to process audio.")


    except Exception as e:
        print(f"❌ Plugin error: {str(e)}")


if __name__ == "__main__":
    main()
