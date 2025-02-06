# AnimaEcho Plugin

AnimaEcho is a VTube Studio integration plugin that enables voice interaction with AI, allowing your avatar to respond in real-time using text-to-speech and lip sync animation.

## Installation

1. Remove previous versions (if installed)
    ```bash
    pip uninstall animaecho-plugin -y
    ```
   
2. Recreate and build the package
    ```bash
    python animaecho_plugin/setup.py sdist bdist_wheel
    ```
3. Install the plugin
    ```bash
    pip install dist/animaecho_plugin-1.0-py3-none-any.whl
    ```
4.  Verify installation
    ```bash
    which animaecho  # macOS/Linux
    where animaecho  # Windows
    ```

## Usage

#### Run the plugin
```bash
animaecho
```

🎙️ The plugin will start recording audio, send it to the Anima API, and play back the response in sync with your VTube Studio avatar.

---

### Reinstalling the plugin

If you need to reinstall the plugin, use:

```bash
pip install --force-reinstall dist/animaecho_plugin-1.0-py3-none-any.whl
```

### How It Works

1. Records your voice using a microphone.
2. Sends the recorded audio to the AI-powered AnimaEcho API.
3. Receives an AI-generated voice response in return.
4. Plays the AI-generated response in VTube Studio.
5. Syncs lip movements to match the response.

---

## Troubleshooting

#### If you encounter issues, check the following:
- Ensure **VTube Studio** is running and the WebSocket API is **enabled**.
- Verify that the plugin has been **granted permission** in VTube Studio.
- Check the **Python environment** and ensure dependencies are installed.
- If you see an **FFmpeg error**, ensure `ffmpeg` is installed and accessible from the command line.
- Try reinstalling the plugin with:
  ```bash
    pip install --force-reinstall dist/animaecho_plugin-1.0-py3-none-any.whl
    ```