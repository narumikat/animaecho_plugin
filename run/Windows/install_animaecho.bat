@echo off
python -m venv animaecho_env
call animaecho_env\Scripts\activate
pip install dist/animaecho_plugin-1.0-py3-none-any.whl
echo AnimaEcho installed successfully!
pause
