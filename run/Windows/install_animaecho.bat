@echo off
echo Creating a virtual environment...
python -m venv animaecho_env

echo Activating the virtual environment...
call animaecho_env\Scripts\activate

echo Installing dependencies from requirements.txt...
pip install ..\..\requirements.txt

echo Installing AnimaEcho plugin...
pip install ..\..\dist\animaecho_plugin-1.0-py3-none-any.whl

echo AnimaEcho installed successfully!
pause
