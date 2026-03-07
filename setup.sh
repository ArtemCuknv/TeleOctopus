#!/bin/bash

python3 -m venv venv
source venv/bin/activate
./venv/bin/pip install --upgrade pip
./venv/bin/pip install fastapi uvicorn[standard] httpx sqlalchemy pytest pytest-asyncio aiogram prometheus-fastapi-instrumentator
# python3 -m pytest -v -s
echo "Setup complete. Use ./run.sh to start."