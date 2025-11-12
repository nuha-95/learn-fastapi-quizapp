const { test, expect } = require('@playwright/test');

test.describe('QuizApp UI Tests', () => {
  
  test('should verify API health endpoint via browser', async ({ page }) => {
    try {
      await page.goto('http://127.0.0.1:8000/health', { timeout: 10000 });
      
      // Check JSON response
      const content = await page.textContent('body');
      const response = JSON.parse(content);
      
      expect(response.status).toBe('healthy');
      expect(response.message).toContain('QuizApp');
    } catch (error) {
      console.log('Health endpoint test failed:', error.message);
      throw error;
    }
  });

  test('should access API documentation', async ({ page }) => {
    try {
      await page.goto('http://127.0.0.1:8000/docs', { timeout: 10000 });
      
      // Wait for page to load
      await page.waitForLoadState('networkidle');
      
      // Check if page loads (basic check)
      const title = await page.title();
      expect(title).toContain('FastAPI');
    } catch (error) {
      console.log('Docs test failed:', error.message);
      throw error;
    }
  });
});