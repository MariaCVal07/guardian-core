import { test, expect } from '@playwright/test';

test('T001: Validate credit card payment', async ({ page }) => {
  // Arrange
  const url = 'https://example.com/payment';
  const creditCardNumber = '4111111111111111';
  const expirationDate = '12/2025';
  const cvv = '123';

  // Act
  await page.goto(url);
  await page.fill('input[name="creditCardNumber"]', creditCardNumber);
  await page.fill('input[name="expirationDate"]', expirationDate);
  await page.fill('input[name="cvv"]', cvv);
  await page.click('button[type="submit"]');

  // Assert
  await expect(page).toHaveURL('https://example.com/payment/success');
  await expect(page.locator('text=Payment successful')).toBeVisible();
});