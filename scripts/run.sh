#!/bin/bash
source .env
uvicorn app.main:app --reload --host 0.0.0.0
