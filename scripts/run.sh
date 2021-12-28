#!/bin/bash
source scripts/env.sh
uvicorn app.main:app --reload --host 0.0.0.0
