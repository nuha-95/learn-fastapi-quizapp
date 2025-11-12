@echo off
echo Starting QuizApp for testing...
start /B uvicorn main:app --reload --port 8000

echo Waiting for API to start...
timeout /t 5 /nobreak > nul

echo Running PyTest API tests...
cd api\pytest
pytest -v --tb=short

echo Tests completed.
pause