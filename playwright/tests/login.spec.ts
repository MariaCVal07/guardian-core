import { test, expect} from '@playwright/test';
import { loginFlow } from '../flows/login.flow';

test ("Validar login exitoso", async ({ page }) => {
    await loginFlow(page);

    await expect(page).toHaveURL(/logged-in-successfully/);

    await expect(page.locator(".post-title")).toContainText("Logged in Successfully");

    await page.screenshot({
    path: 'execution-results/login-success-${Date.now()}.png'
    }); 
});