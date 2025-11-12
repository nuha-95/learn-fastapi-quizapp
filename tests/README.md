# QuizApp Testing Suite

Comprehensive automated testing setup for QuizApp FastAPI backend using **Postman/Newman**, **PyTest**, and **Playwright**.

## 📁 Directory Structure

```
tests/
├── api/
│   ├── postman/
│   │   ├── QuizApp_Collection.json     # Postman test collection
│   │   └── QuizApp_Environment.json    # Environment variables
│   └── pytest/
│       ├── conftest.py                 # PyTest configuration
│       └── test_quiz_endpoints.py      # API tests using requests
├── ui/
│   └── playwright/
│       ├── playwright.config.js        # Playwright configuration
│       └── test_ui_quiz.js            # UI tests
├── reports/                           # Test reports output
├── run_postman_tests.bat             # Local Postman test runner
├── run_pytest_tests.bat              # Local PyTest runner
├── run_playwright_tests.bat          # Local Playwright runner
└── README.md                         # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Node.js** (for Newman and Playwright)
2. **Python 3.9+** with pip
3. **PostgreSQL** (for database)

### Install Dependencies

```bash
# Python dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# Node.js dependencies
npm install -g newman newman-reporter-htmlextra
npm install -g @playwright/test
npx playwright install
```

## 🧪 Running Tests Locally

### 1. Postman/Newman Tests

```bash
# Windows
tests\run_postman_tests.bat

# Manual command
newman run tests/api/postman/QuizApp_Collection.json \
  -e tests/api/postman/QuizApp_Environment.json \
  -r htmlextra \
  --reporter-htmlextra-export reports/postman-report.html
```

### 2. PyTest API Tests

```bash
# Windows
tests\run_pytest_tests.bat

# Manual command
cd tests/api/pytest
pytest -v --tb=short
```

### 3. Playwright UI Tests

```bash
# Windows
tests\run_playwright_tests.bat

# Manual command
cd tests/ui/playwright
npx playwright test
```

## 🔄 CI/CD with GitHub Actions

Two workflows are configured:

### 1. Postman + PyTest Workflow (`.github/workflows/ci-postman.yml`)
- Runs on push/PR to main/develop
- Sets up PostgreSQL service
- Installs Python and Node.js dependencies
- Starts FastAPI app
- Runs Newman tests with HTML reports
- Runs PyTest API tests
- Uploads test artifacts

### 2. Playwright Workflow (`.github/workflows/ci-playwright.yml`)
- Runs UI tests separately
- Uploads Playwright reports

## 📊 Test Coverage

### API Tests (Postman + PyTest)
- ✅ `GET /health` - Health check endpoint
- ✅ `POST /questions/` - Create question (valid/invalid)
- ✅ `GET /questions/{id}` - Get question (valid/invalid ID)
- ✅ `GET /choices/{question_id}` - Get choices (valid/invalid ID)
- ✅ Response time assertions (< 500ms for GET, < 1000ms for POST)
- ✅ JSON schema validation
- ✅ Error handling (400, 404, 422 status codes)

### UI Tests (Playwright)
- ✅ Terminal documentation page loading
- ✅ API documentation (Swagger UI) accessibility
- ✅ Health endpoint via browser

## 📈 Test Reports

### Postman Reports
- HTML reports generated in `reports/postman-report.html`
- Includes response times, test results, and failure details
- Dark theme enabled for better readability

### PyTest Reports
- Console output with detailed test results
- Supports verbose mode with `pytest -v`

### Playwright Reports
- Automatic screenshots on failure
- Video recordings for failed tests
- HTML report with test timeline

## 🛠️ Customization

### Adding New Postman Tests

1. Edit `tests/api/postman/QuizApp_Collection.json`
2. Add new request with test scripts:

```javascript
pm.test('Status code is 200', function () {
    pm.response.to.have.status(200);
});

pm.test('Response time is acceptable', function () {
    pm.expect(pm.response.responseTime).to.be.below(500);
});
```

### Adding New PyTest Tests

1. Add test methods to `tests/api/pytest/test_quiz_endpoints.py`:

```python
def test_new_endpoint(self):
    response = requests.get(f"{BASE_URL}/new-endpoint")
    assert response.status_code == 200
```

### Adding New Playwright Tests

1. Add test cases to `tests/ui/playwright/test_ui_quiz.js`:

```javascript
test('should test new UI feature', async ({ page }) => {
    await page.goto('http://127.0.0.1:8000/new-page');
    await expect(page.locator('.new-element')).toBeVisible();
});
```

## 🔧 Environment Variables

### Local Testing
- `BASE_URL`: API base URL (default: http://127.0.0.1:8000)

### CI/CD
- `DATABASE_URL`: PostgreSQL connection string
- Automatically configured in GitHub Actions

## 📝 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Data Cleanup**: Use test databases, not production
3. **Assertions**: Include multiple assertions per test
4. **Response Times**: Monitor API performance
5. **Error Cases**: Test both success and failure scenarios
6. **Schema Validation**: Verify response structure
7. **Environment Separation**: Use different configs for test/prod

## 🐛 Troubleshooting

### Common Issues

1. **API not starting**: Check if port 8000 is available
2. **Database connection**: Ensure PostgreSQL is running
3. **Newman not found**: Install globally with `npm install -g newman`
4. **Playwright browser issues**: Run `npx playwright install`

### Debug Commands

```bash
# Check API health
curl http://127.0.0.1:8000/health

# Verbose PyTest output
pytest -v -s

# Playwright debug mode
npx playwright test --debug
```

## 📚 Additional Resources

- [Newman Documentation](https://learning.postman.com/docs/running-collections/using-newman-cli/)
- [PyTest Documentation](https://docs.pytest.org/)
- [Playwright Documentation](https://playwright.dev/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)