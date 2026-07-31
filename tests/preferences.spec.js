const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');
const jsdom = require('jsdom');

const fileUrl = 'file://' + path.resolve(__dirname, '../webGantt.html');

const emptyGan = `<?xml version="1.0" encoding="UTF-8"?>
<project name="Untitled Gantt Project" company="" webLink="http://" view-date="2023-01-01" view-index="0" gantt-divider-location="300" resource-divider-location="300" version="3.3.3312">
<description/>
<view zooming-state="default:2" id="gantt-chart">
<field id="tpd3" name="Name" width="200" order="0"/>
</view>
<view id="resource-table">
<field id="0" name="Name" width="210" order="0"/>
</view>
</project>`;

test.describe('Preferences Modal Tests', () => {
    let tempGanPath;

    test.beforeAll(() => {
        tempGanPath = path.resolve(__dirname, 'temp.gan');
        fs.writeFileSync(tempGanPath, emptyGan);
    });

    test.afterAll(() => {
        if (fs.existsSync(tempGanPath)) fs.unlinkSync(tempGanPath);
    });

    test.beforeEach(async ({ page }) => {
        page.on('console', msg => console.log('BROWSER LOG:', msg.text()));
        await page.goto(fileUrl);
        // Wait a short time for any DB load to finish before injecting our mock
        await page.waitForTimeout(1000);

        await page.evaluate(() => {
            // Load a mock project with a task and a milestone so SVG rendering occurs
            const xml = `<?xml version="1.0" encoding="UTF-8"?>
            <project>
                <tasks>
                    <task id="0" name="Task 1" color="#8cb6ce" meeting="false" start="2026-07-01" duration="5" complete="0" expand="true"/>
                    <task id="1" name="Milestone 1" color="#8cb6ce" meeting="true" start="2026-07-05" duration="0" complete="0" expand="true"/>
                </tasks>
                <view id="gantt-chart"></view>
                <view id="resource-table"></view>
            </project>`;
            state.loadXML(xml);
        });
        await page.click('#btn-preferences');
    });

    const fieldsToTest = [
        // Onglet General
        { id: 'pref-gen-appearance', xmlId: 'general.appearance', vals: ['Plastic', 'Windows', 'Mac OS X', 'Nimbus', 'CDE/Motif'], view: 'gantt-chart' },
        { id: 'pref-gen-app-font', xmlId: 'general.appFont', vals: ['default', 'Arial', 'Helvetica', 'Times New Roman', 'Courier', 'Verdana', 'Tahoma'], view: 'gantt-chart' },
        { id: 'pref-gen-app-font-size', xmlId: 'general.appFontSize', vals: ['1', '2', '3', '4', '5'], view: 'gantt-chart' },
        { id: 'pref-gen-chart-font', xmlId: 'general.chartFont', vals: ['default', 'Arial', 'Helvetica', 'Times New Roman', 'Courier', 'Verdana', 'Tahoma'], view: 'gantt-chart' },
        { id: 'pref-gen-chart-font-size', xmlId: 'general.chartFontSize', vals: ['1', '2', '3', '4', '5'], view: 'gantt-chart' },
        { id: 'pref-gen-row-spacing', xmlId: 'general.rowSpacing', vals: ['15.0', '24.5', '32.0'], view: 'gantt-chart' },
        { id: 'pref-gen-dpi', xmlId: 'general.dpi', vals: ['96', '120'], view: 'gantt-chart' },
        { id: 'pref-gen-language', xmlId: 'general.language', vals: ['fr', 'en', 'es', 'de', 'it', 'pt'], view: 'gantt-chart' },
        { radioName: 'pref-gen-date-format-type', xmlId: 'general.dateFormatType', vals: ['default', 'custom'], view: 'gantt-chart' },
        { id: 'pref-gen-date-format', xmlId: 'general.dateFormat', vals: ['dd/MM/y', 'yyyy-MM-dd'], view: 'gantt-chart' },
        { id: 'pref-gen-logo', xmlId: 'general.logo', vals: ['', '/path/to/logo.png'], view: 'gantt-chart' },

        // Onglet Gantt
        { id: 'pref-gantt-task-prefix', xmlId: 'gantt.taskPrefix', vals: ['tâche', 'Task_'], view: 'gantt-chart' },
        { id: 'pref-gantt-task-copy-format', xmlId: 'gantt.taskCopyFormat', vals: ['{0}_{1}', 'Copy of {0}'], view: 'gantt-chart' },
        { id: 'pref-gantt-new-task-color', xmlId: 'gantt.newTaskColor', vals: ['#8cb6ce', '#ff0000'], view: 'gantt-chart' },
        { id: 'pref-gantt-constraint', xmlId: 'gantt.constraint', vals: ['Strong', 'Rubber'], view: 'gantt-chart' },
        { radioName: 'pref-gantt-today-line', xmlId: 'gantt.todayLine', vals: ['yes', 'no'], view: 'gantt-chart' },
        { radioName: 'pref-gantt-project-dates', xmlId: 'gantt.projectDates', vals: ['yes', 'no'], view: 'gantt-chart' },
        { id: 'pref-gantt-weekend-style', xmlId: 'gantt.weekendStyle', vals: ['default', 'hidden', 'transparent'], view: 'gantt-chart' },
        { id: 'pref-gantt-week-numbering', xmlId: 'gantt.weekNumbering', vals: ['default', 'none', 'us'], view: 'gantt-chart' },
        { id: 'pref-gantt-show-milestones', xmlId: 'gantt.showMilestones', vals: [true, false], view: 'gantt-chart', isCheckbox: true },
        { id: 'pref-gantt-detail-top', xmlId: 'gantt.detailTop', vals: ['', 'name', 'resources', 'progress', 'duration'], view: 'gantt-chart' },
        { id: 'pref-gantt-detail-bottom', xmlId: 'gantt.detailBottom', vals: ['', 'name', 'resources', 'progress', 'duration'], view: 'gantt-chart' },
        { id: 'pref-gantt-detail-left', xmlId: 'gantt.detailLeft', vals: ['', 'name', 'resources', 'progress', 'duration'], view: 'gantt-chart' },
        { id: 'pref-gantt-detail-right', xmlId: 'gantt.detailRight', vals: ['', 'name', 'resources', 'progress', 'duration'], view: 'gantt-chart' },

        // Onglet Ressources
        { id: 'pref-res-color', xmlId: 'res.color', vals: ['#c8e6c9', '#112233'], view: 'resource-table' },
        { id: 'pref-res-overloaded-color', xmlId: 'res.overloadedColor', vals: ['#ffcdd2', '#aa0000'], view: 'resource-table' },
        { id: 'pref-res-underloaded-color', xmlId: 'res.underloadedColor', vals: ['#3bd93b', '#00bb00'], view: 'resource-table' },
        { id: 'pref-res-vacation-color', xmlId: 'res.vacationColor', vals: ['#e2e2e2', '#cccccc'], view: 'resource-table' },
    ];

    for (const field of fieldsToTest) {
        for (const testVal of field.vals) {
            test(`should correctly save ${field.xmlId} setting to XML with value ${testVal}`, async ({ page }) => {
                const currentField = { ...field, val: testVal };
                if (currentField.radioName) {
                    await page.evaluate((f) => {
                        const el = document.querySelector(`input[name="${f.radioName}"][value="${f.val}"]`);
                        if (el) el.checked = true;
                    }, currentField);
                } else if (currentField.isCheckbox) {
                    await page.evaluate((f) => {
                        const el = document.getElementById(f.id);
                        if (el) el.checked = f.val;
                    }, currentField);
                } else {
                    // Set the value directly in the DOM to avoid Playwright type mismatches (like select vs input)
                    await page.evaluate((f) => {
                        const el = document.getElementById(f.id);
                        if (el) {
                            el.value = f.val;
                            el.dispatchEvent(new Event('change'));
                        }
                    }, currentField);
                }

                await page.click('#pref-btn-save');

                const savedVal = await page.evaluate((f) => {
                    // state is declared as const at the top level, accessible directly
                    if (!state || !state.xmlDoc) return null;
                    const view = state.xmlDoc.querySelector(`view[id="${f.view}"]`);
                    if (!view) return null;
                    const opt = view.querySelector(`option[id="${f.xmlId}"]`);
                    return opt ? opt.getAttribute('value') : null;
                }, currentField);
                
                const expected = currentField.isCheckbox ? (currentField.val ? 'true' : 'false') : currentField.val;
                expect(savedVal).toBe(expected);

                // Assert that the UI was updated correctly (Functional testing)
                const uiAssertionResult = await page.evaluate((f) => {
                    if (f.xmlId === 'general.appFont') {
                        if (f.val === 'default') return true;
                        return document.body.style.fontFamily.includes(f.val);
                    }
                    if (f.xmlId === 'general.chartFont') {
                        if (f.val === 'default') return true;
                        const svg = document.querySelector('#gantt-content svg');
                        return svg ? svg.style.fontFamily.includes(f.val) : false;
                    }
                    if (f.xmlId === 'gantt.projectDates') {
                        const lines = document.querySelectorAll('#gantt-content svg line[stroke="green"]');
                        return f.val === 'yes' ? lines.length >= 2 : lines.length === 0;
                    }
                    if (f.xmlId === 'gantt.showMilestones') {
                        const poly = document.querySelectorAll('#gantt-content svg polygon');
                        return f.val ? poly.length > 0 : poly.length === 0;
                    }
                    return true;
                }, currentField);
                expect(uiAssertionResult).toBe(true);
            });
        }
    }
});
