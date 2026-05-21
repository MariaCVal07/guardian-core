import { Page } from '@playwright/test';

export async function loginFlow(page:Page) {
    await page.goto("https://practicetestautomation.com/practice-test-login/");
    await page.locator("#username").fill("student");
    await page.locator("#password").fill("Password123");
    await page.locator("#submit").click();

}