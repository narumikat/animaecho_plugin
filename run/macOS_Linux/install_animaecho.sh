echo "Creating a virtual environment..."
python3 -m venv animaecho_env

echo "Activating the virtual environment..."
source animaecho_env/bin/activate

echo "Installing dependencies from requirements.txt..."
pip install -r ../../requirements.txt

echo "Installing AnimaEcho plugin..."
pip install ../../dist/animaecho_plugin-1.0-py3-none-any.whl

echo "AnimaEcho installed successfully!"
