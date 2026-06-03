LOGIN_TEMPLATE = """
import { test, expect } from '@playwright/test';

test('Validar login exitoso SauceDemo', async ({ page }) => {

  test.setTimeout(10000);

  // Arrange
  const url = 'https://www.saucedemo.com/';
  const username = 'standard_user';
  const password = 'secret_sauce';

  // Act
  await page.goto(url);

  await page.fill('[data-test="username"]', username);
  await page.fill('[data-test="password"]', password);

  await page.click('[data-test="login-button"]');

  // Assert
  await expect(page).toHaveURL(/inventory/);

  await expect(
    page.locator('.title')
  ).toContainText('Products');

});
"""
