@echo off
echo Starting QuizApp for testing...
start /B uvicorn main:app --reload --port 8000

echo Waiting for API to start...
timeout /t 5 /nobreak > nul

echo Running Postman tests with Newman...
newman run api/postman/QuizApp_Collection.json -e api/postman/QuizApp_Environment.json -r htmlextra --reporter-htmlextra-export ../reports/postman-report.html

echo Tests completed. Check reports folder for results.
pause