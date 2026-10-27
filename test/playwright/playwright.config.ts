import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests",
  retries: 0,
  reporter: [["json", { outputFile: "report.json" }]],
  use: { channel: "chrome", trace: "retain-on-failure", screenshot: "only-on-failure" },
  timeout: 8000,
  expect: { timeout: 1500 },
});
