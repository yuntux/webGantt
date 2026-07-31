const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1280, height: 800 } });
  
  const xmlContent = fs.readFileSync(path.resolve(__dirname, '../specs/001-ganttproject-features/assets/example.gan'), 'utf8');

  await page.addInitScript((xml) => {
    localStorage.setItem('webGantt_lang', 'en_US');
    window.showOpenFilePicker = async () => {
      return [{
        getFile: async () => {
          return new File([xml], 'example.gan', { type: 'text/xml' });
        }
      }];
    };
  }, xmlContent);

  const fileUri = 'file://' + path.resolve(__dirname, '../webGantt.html');
  await page.goto(fileUri);
  
  // Click open
  await page.click('#btn-open');
  await page.waitForTimeout(1000);

  // (No need to create artifacts dir as we are inside it)

  // Screenshot 1: Main Gantt View
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_main.png') });
  console.log('Took screenshot_main.png');

  // Screenshot 2: Project Properties
  await page.click('#btn-props');
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_project_props.png') });
  console.log('Took screenshot_project_props.png');
  await page.click('#proj-prop-modal .close');
  await page.waitForTimeout(500);

  // Screenshot 3: Task Details
  // Click on a task in WBS
  await page.evaluate(() => {
    // Open Phase 1 details
    window.openTaskDetails('0');
  });
  await page.waitForTimeout(500);
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_task_details.png') });
  console.log('Took screenshot_task_details.png');
  await page.click('#task-modal .close');
  await page.waitForTimeout(500);

  // Screenshot 4: Resources View
  await page.evaluate(() => {
    document.querySelectorAll('.tab-btn')[1].click();
  });
  await page.waitForTimeout(500);
  // Add a holiday for screenshot? Just take screenshot.
  await page.screenshot({ path: path.resolve(__dirname, 'screenshot_resources.png') });
  console.log('Took screenshot_resources.png');

  await browser.close();
})();
