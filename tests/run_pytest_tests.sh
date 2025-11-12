#!/bin/bash
echo "Starting QuizApp for testing..."
uvicorn main:app --reload --port 8000 &
API_PID=$!

echo "Waiting for API to start..."
sleep 5

echo "Running PyTest API tests..."
cd tests/api/pytest
pytest -v --tb=short

echo "Stopping API..."
kill $API_PID

echo "Tests completed."