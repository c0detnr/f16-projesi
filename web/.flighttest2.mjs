import { chromium } from "playwright";

const browser = await chromium.launch({
  args: ["--no-sandbox", "--enable-unsafe-swiftshader", "--use-angle=swiftshader"],
});
const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
const errors = [];
page.on("pageerror", (e) => errors.push("PAGEERROR: " + e.message));

await page.goto("http://localhost:5199/#demo");

const readHud = () => page.textContent("#hud").then((t) => t.trim().replace(/\n/g, " | "));

let hud;
for (let i = 0; i < 40; i++) {
  await page.waitForTimeout(3000);
  hud = await readHud();
  const speed = parseInt(hud.match(/HIZ (\d+)/)[1]);
  if (speed >= 200) break;
}
console.log("ROL:", hud);

await page.mouse.move(640, 400);
for (let i = 0; i < 24; i++) {
  await page.mouse.move(640, 400 + i * 12);
  await page.waitForTimeout(250);
}
await page.waitForTimeout(6000);
console.log("KALKIS:", await readHud());
await page.screenshot({ path: "/tmp/opencode/shot_climb.png" });

console.log("ERRORS:", errors.length ? errors.slice(0, 6) : "none");
await browser.close();
