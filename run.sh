#!/bin/bash
source venv/bin/activate

# python3 -m pytest -v -s
mkdir -p /tmp/prometheus_multiproc
export PROMETHEUS_MULTIPROC_DIR=/tmp/prometheus_multiproc
rm -rf /tmp/prometheus_multiproc/*
export PYTHONPATH=$PYTHONPATH:.
exec uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2