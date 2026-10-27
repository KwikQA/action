import { test, expect } from "@playwright/test";

const PAGE = `
<html><head><title>Shop</title></head><body>
<header><nav aria-label="Main"><a href="#">Home</a><a href="#">Cart</a></nav></header>
<main>
  <h1>Checkout</h1>
  <form aria-label="Coupon">
    <label for="code">Coupon code</label><input id="code" name="code" data-testid="coupon-input">
    <button type="button" data-testid="apply-discount" onclick="apply()">Apply discount</button>
  </form>
  <p id="total" data-testid="order-total">Total: $40.00</p>
  <ul><li>Item A</li><li>Item B</li></ul>
  <button>Pay now</button>
</main>
<script>
  function apply(){ document.getElementById('total').textContent = 'Total: $36.00'; console.error('coupon service: 500'); fetch('/api/coupon').catch(()=>{}); }
  console.log('page ready');
</script>
</body></html>`;

test.beforeEach(async ({ page }) => {
  await page.route("**/api/coupon", (route) => route.fulfill({ status: 500, contentType: "application/json", body: '{"error":"coupon expired"}' }));
  await page.route("http://shop.test/", (route) => route.fulfill({ status: 200, contentType: "text/html", body: PAGE }));
  await page.goto("http://shop.test/");
});

test("renamed test id", async ({ page }) => {
  await page.getByTestId("coupon-input").fill("SAVE10");
  await page.getByTestId("apply-coupon").click();
});

test("renamed button text", async ({ page }) => {
  await page.getByRole("button", { name: "Apply coupon" }).click();
});

test("wrong total", async ({ page }) => {
  await page.getByTestId("apply-discount").click();
  await expect(page.getByTestId("order-total")).toHaveText("Total: $30.00");
});

test("ambiguous button", async ({ page }) => {
  await page.getByRole("button").click();
});

test("css selector missing", async ({ page }) => {
  await page.locator("#apply-btn").click();
});
