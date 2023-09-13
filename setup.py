from setuptools import setup

setup(
    name='lyrics_dl',
    version='0.0.1',    
    description='An ultimate cli tool for downloading song lyrics, inspired by other awesome *-dl programs.',
    packages=[
        "lyrics_dl",
        "lyrics_dl.providers",
    ],
    install_requires=[
        "httpx>=0.24.1",
        "mutagen>=1.46.0",
    ]
)
