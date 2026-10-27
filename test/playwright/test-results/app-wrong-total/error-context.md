# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: app.spec.ts >> wrong total
- Location: tests/app.spec.ts:37:5

# Error details

```
Error: expect(locator).toHaveText(expected) failed

Locator:  getByTestId('order-total')
Expected: "Total: $30.00"
Received: "Total: $36.00"
Timeout:  1500ms

Call log:
  - Expect "toHaveText" getByTestId('order-total') with timeout 1500ms
  - waiting for getByTestId('order-total')
    16 × locator resolved to <p id="total" data-testid="order-total">Total: $36.00</p>
       - unexpected value "Total: $36.00"

```

```yaml
- paragraph: "Total: $36.00"
```

# Test source

```ts
  1  | import { test, expect } from "@playwright/test";
  2  | 
  3  | const PAGE = `
  4  | <html><head><title>Shop</title></head><body>
  5  | <header><nav aria-label="Main"><a href="#">Home</a><a href="#">Cart</a></nav></header>
  6  | <main>
  7  |   <h1>Checkout</h1>
  8  |   <form aria-label="Coupon">
  9  |     <label for="code">Coupon code</label><input id="code" name="code" data-testid="coupon-input">
  10 |     <button type="button" data-testid="apply-discount" onclick="apply()">Apply discount</button>
  11 |   </form>
  12 |   <p id="total" data-testid="order-total">Total: $40.00</p>
  13 |   <ul><li>Item A</li><li>Item B</li></ul>
  14 |   <button>Pay now</button>
  15 | </main>
  16 | <script>
  17 |   function apply(){ document.getElementById('total').textContent = 'Total: $36.00'; console.error('coupon service: 500'); fetch('/api/coupon').catch(()=>{}); }
  18 |   console.log('page ready');
  19 | </script>
  20 | </body></html>`;
  21 | 
  22 | test.beforeEach(async ({ page }) => {
  23 |   await page.route("**/api/coupon", (route) => route.fulfill({ status: 500, contentType: "application/json", body: '{"error":"coupon expired"}' }));
  24 |   await page.route("http://shop.test/", (route) => route.fulfill({ status: 200, contentType: "text/html", body: PAGE }));
  25 |   await page.goto("http://shop.test/");
  26 | });
  27 | 
  28 | test("renamed test id", async ({ page }) => {
  29 |   await page.getByTestId("coupon-input").fill("SAVE10");
  30 |   await page.getByTestId("apply-coupon").click();
  31 | });
  32 | 
  33 | test("renamed button text", async ({ page }) => {
  34 |   await page.getByRole("button", { name: "Apply coupon" }).click();
  35 | });
  36 | 
  37 | test("wrong total", async ({ page }) => {
  38 |   await page.getByTestId("apply-discount").click();
> 39 |   await expect(page.getByTestId("order-total")).toHaveText("Total: $30.00");
     |                                                 ^ Error: expect(locator).toHaveText(expected) failed
  40 | });
  41 | 
  42 | test("ambiguous button", async ({ page }) => {
  43 |   await page.getByRole("button").click();
  44 | });
  45 | 
  46 | test("css selector missing", async ({ page }) => {
  47 |   await page.locator("#apply-btn").click();
  48 | });
  49 | 
```