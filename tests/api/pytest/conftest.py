import pytest
import requests
import time

@pytest.fixture(scope="session", autouse=True)
def wait_for_api():
    """Wait for API to be ready before running tests"""
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get("http://127.0.0.1:8000/health", timeout=1)
            if response.status_code == 200:
                return
        except:
            pass
        time.sleep(1)
    pytest.fail("API not ready after 30 seconds")