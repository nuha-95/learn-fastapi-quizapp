#!/bin/bash
echo "Starting QuizApp for testing..."
uvicorn main_test:app --reload --port 8000 &
API_PID=$!

echo "Waiting for API to start..."
sleep 5

echo "Running Playwright UI tests..."
cd tests/ui/playwright
npx playwright test

echo "Stopping API..."
kill $API_PID

echo "Tests completed."