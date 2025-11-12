@echo off
echo Starting QuizApp for testing...
start /B uvicorn main:app --reload --port 8000

echo Waiting for API to start...
timeout /t 5 /nobreak > nul

echo Running Playwright UI tests...
cd ui\playwright
npx playwright test

echo Tests completed.
pause