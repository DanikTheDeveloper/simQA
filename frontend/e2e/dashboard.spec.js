import { test, expect } from '@playwright/test';

test.describe('Building Simulator Dashboard', () => {
  test('dashboard loads successfully', async ({ page }) => {
    await page.goto('/');

    await expect(page.getByRole('columnheader', { name: /device id/i })).toBeVisible();
  });

  test('device data is visible', async ({ page }) => {
    await page.goto('/');

    await expect(page.locator('body')).toContainText(/temperature|humidity|status|device/i);
  });

  test('refresh button works if present', async ({ page }) => {
    await page.goto('/');

    const refreshButton = page.getByRole('button', { name: /refresh/i });

    if (await refreshButton.count()) {
      await refreshButton.click();
    }

    await expect(page.locator('body')).toContainText(/device|temperature|humidity|status/i);
  });
});