#!/usr/bin/env bash
export IS_DEBUG=${DEBUG:-false}
exec uvicorn --host 127.0.0.1 --port 8000 --access-log --log-level info api:APP --reload
# exec python run.pycl
