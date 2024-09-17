#!/bin/bash
#chmod +x docker/app.sh
cd src
#alembic upgrade head
gunicorn main:main_app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8003
