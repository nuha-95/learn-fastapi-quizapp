#!/bin/bash
echo "Starting QuizApp for testing..."
uvicorn main:app --reload --port 8000 &
API_PID=$!

echo "Waiting for API to start..."
sleep 5

echo "Running Postman tests with Newman..."
newman run tests/api/postman/QuizApp_Collection.json -e tests/api/postman/QuizApp_Environment.json -r htmlextra --reporter-htmlextra-export reports/postman-report.html

echo "Stopping API..."
kill $API_PID

echo "Tests completed. Check reports folder for results."