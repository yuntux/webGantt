const { test, expect } = require('@playwright/test');
const path = require('path');
const fs = require('fs');

test.describe('webGantt E2E Tests', () => {
  test('Cycle E2E : Chargement, Modification et Sauvegarde', async ({ page }) => {
    // 1. Ouvrir l'application web locale
    const absolutePath = path.resolve(__dirname, '../webGantt.html');
    await page.goto(`file://${absolutePath}`);

    // Forcer le fallback pour que Playwright intercepte l'input natif et le téléchargement
    await page.evaluate(() => {
        window.showOpenFilePicker = undefined;
        window.showSaveFilePicker = undefined;
    });

    // 2. Intercepter le dialogue d'ouverture de fichier
    const [fileChooser] = await Promise.all([
        page.waitForEvent('filechooser'),
        page.click('#btn-open')
    ]);
    
    // Charger le fichier .gan d'exemple
    const exampleGanPath = path.resolve(__dirname, '../specs/001-ganttproject-features/assets/example.gan');
    await fileChooser.setFiles(exampleGanPath);

    // Vérifier que le WBS s'est bien rempli (les données ont été parsées)
    await page.waitForSelector('#wbs-content > div');
    const wbsRowsCount = await page.locator('#wbs-content > div').count();
    expect(wbsRowsCount).toBeGreaterThan(0);

    // 3. Modifier le DOM : Ajouter une nouvelle tâche
    await page.click('#btn-add-task');
    
    // Vérifier que la nouvelle ligne WBS a été ajoutée
    const newWbsRowsCount = await page.locator('#wbs-content > div').count();
    expect(newWbsRowsCount).toBe(wbsRowsCount + 1);

    // 4. Intercepter le téléchargement lors de la sauvegarde (fallback File System)
    const [download] = await Promise.all([
        page.waitForEvent('download'),
        page.click('#btn-download')
    ]);

    // Enregistrer le fichier téléchargé et vérifier son existence
    const downloadPath = await download.path();
    expect(fs.existsSync(downloadPath)).toBeTruthy();
    
    // Lire le contenu XML sauvegardé et vérifier qu'il contient la tâche modifiée
    const savedContent = fs.readFileSync(downloadPath, 'utf8');
    expect(savedContent).toContain('<?xml');
    expect(savedContent).toContain('<project');
    expect(savedContent).toContain('Nouvelle Tâche'); // Vérifie l'injection de notre tâche
  });
});
