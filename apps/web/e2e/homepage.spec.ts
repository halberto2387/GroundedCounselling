import { test, expect } from '@playwright/test';

test.describe('GroundedCounselling Homepage', () => {
  test('should load the homepage successfully', async ({ page }) => {
    await page.goto('/');

    // Check that the page title is correct
    await expect(page).toHaveTitle(/GroundedCounselling/);

    // Check for main heading
    await expect(page.locator('h1')).toContainText('Welcome to GroundedCounselling');

    // Check for description
    await expect(page.locator('text=Professional counselling practice management system')).toBeVisible();
  });

  test('should navigate to services page', async ({ page }) => {
    await page.goto('/');

    // Click on services link
    await page.click('text=Services');

    // Should navigate to services page
    await expect(page).toHaveURL('/services');
    await expect(page.locator('h1')).toContainText('Our Services');
  });

  test('should navigate to specialists page', async ({ page }) => {
    await page.goto('/');

    // Click on specialists link
    await page.click('text=Specialists');

    // Should navigate to specialists page
    await expect(page).toHaveURL('/specialists');
    await expect(page.locator('h1')).toContainText('Our Specialists');
  });

  test('should show sign in page when clicking sign in button', async ({ page }) => {
    await page.goto('/');

    // Click on sign in button
    await page.click('text=Sign In');

    // Should navigate to sign in page
    await expect(page).toHaveURL('/auth/signin');
    await expect(page.locator('h2')).toContainText('Sign in to your account');
  });

  test('should display feature cards', async ({ page }) => {
    await page.goto('/');

    // Check for feature cards
    await expect(page.locator('text=For Counsellors')).toBeVisible();
    await expect(page.locator('text=For Clients')).toBeVisible();
    await expect(page.locator('text=Security & Compliance')).toBeVisible();
  });

  test('should have working CTA buttons', async ({ page }) => {
    await page.goto('/');

    // Check for CTA buttons
    const bookButton = page.locator('text=Book a Session');
    const learnMoreButton = page.locator('text=Learn More');

    await expect(bookButton).toBeVisible();
    await expect(learnMoreButton).toBeVisible();

    // Test navigation
    await bookButton.click();
    await expect(page).toHaveURL('/book');
  });
});