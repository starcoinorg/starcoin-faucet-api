#!/bin/bash
source env.sh
celery worker -A app.worker -E