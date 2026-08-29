/**
 * Capture local routes at the requested widths.
 * Run with a Playwright-capable environment: `node scripts/visual-qa.mjs`.
 */
import { chromium } from "playwright";
import { mkdir } from "node:fs/promises";

const baseUrl = process.env.VISUAL_QA_BASE_URL ?? "http://localhost:3000";
const routes = ["/", "/projects", "/projects/2026-08-15-online-retail-customer-growth"];
const widths = [375, 430, 768, 1024, 1280, 1440, 1920];

await mkdir("visual-tests/actual", { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage();

for (const route of routes) {
  for (const width of widths) {
    await page.setViewportSize({ width, height: width < 600 ? 812 : 900 });
    await page.goto(`${baseUrl}${route}`, { waitUntil: "networkidle" });
    await page.screenshot({ path: `visual-tests/actual/${route === "/" ? "home" : route.slice(1).replaceAll("/", "-")}-${width}.png`, fullPage: true });
  }
}

await browser.close();
