import { chromium } from "playwright";

const browser = await chromium.launch({
  args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-angle=swiftshader"],
});
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
const errors = [];
page.on("pageerror", (e) => errors.push("PAGEERROR: " + e.message));
page.on("console", (m) => {
  if (m.type() === "error") errors.push("CONSOLE: " + m.text());
});

await page.goto("http://localhost:5199/#demo");
await page.waitForTimeout(2000);
const hud0 = await page.textContent("#hud");

await page.waitForTimeout(25000);
const hud1 = await page.textContent("#hud");
await page.screenshot({ path: "/tmp/opencode/shot_air.png" });

await page.keyboard.press("KeyG");
await page.waitForTimeout(4000);
const hud2 = await page.textContent("#hud");
await page.screenshot({ path: "/tmp/opencode/shot_gear.png" });

console.log("T0:", hud0.trim().replace(/\n/g, " | "));
console.log("T25:", hud1.trim().replace(/\n/g, " | "));
console.log("T29+G:", hud2.trim().replace(/\n/g, " | "));
console.log("ERRORS:", errors.length ? errors.slice(0, 6) : "none");
await browser.close();
