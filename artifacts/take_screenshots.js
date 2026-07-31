const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  
  await page.addInitScript(() => {
    localStorage.setItem('webGantt_lang', 'en_US');
  });

  const fileUri = 'file://' + path.resolve(__dirname, '../webGantt.html');
  await page.goto(fileUri);
  await page.waitForTimeout(500); // Wait for DOM load
  
  const xmlContent = fs.readFileSync(path.resolve(__dirname, '../specs/001-ganttproject-features/assets/example.gan'), 'utf8');
  await page.evaluate((xml) => {
    window.state.loadXML(xml);
  }, xmlContent);

  // Wait for rendering
  await page.waitForTimeout(1000);
  // (No need to create artifacts dir as we are inside it)

  // Screenshot 1: Main Gantt View
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_main.png') });
  console.log('Took screenshot_main.png');

  // Screenshot 2: Project Properties
  await page.click('#btn-project-props');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_project_props.png') });
  console.log('Took screenshot_project_props.png');
  await page.evaluate(() => {
    document.getElementById('project-props-modal').close();
  });
  await page.waitForTimeout(500);

  // Screenshot 3: Task Details
  await page.locator('#wbs-content button').first().click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_task_details.png') });
  console.log('Took screenshot_task_details.png');
  await page.evaluate(() => {
    document.getElementById('task-details-modal').close();
  });
  await page.waitForTimeout(500);

  // Screenshot 4: Resources View
  await page.evaluate(() => {
    document.querySelectorAll('.view-tab')[1].click();
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_resources.png') });
  console.log('Took screenshot_resources.png');

  await browser.close();
})();
