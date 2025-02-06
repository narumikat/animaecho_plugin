from setuptools import setup, find_packages

setup(
    name="animaecho-plugin",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pyaudio",
        "pydub",
        "websockets",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "animaecho=animaecho_plugin.main:main",
        ]
    },
    description="Plugin to integrate VTube Studio with AnimaEcho.",
    author="Narumi Katayama",
    author_email="narumi.kataiama@gmail.com",
    url="https://github.com/narumikat/animaecho_plugin",
)
