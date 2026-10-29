// Capturas de «La estación en uso» (landing, L4) con un iPhone 13 simulado.
// Uso: con la estación corriendo (`uv run tht servir --datos <datos-mosaico> --puerto 8780`),
//   URL=http://127.0.0.1:8780 FOTO=<foto de la hoja del mosaico> SALIDA=<carpeta> node herramientas/capturas_uso.js
// Después se reducen a 420 x 855 px en JPEG y se copian a src/inspeccion_tht/static/capturas/uso-1..6.jpg.
// Perfil elegido: María José de la Rosa (tercer perfil de la lista).
const {chromium, devices} = require('playwright');
const URL = process.env.URL || 'http://127.0.0.1:8780';
const FOTO = process.env.FOTO, SALIDA = process.env.SALIDA || '.';
(async () => {
  const b = await chromium.launch();
  const c = await b.newContext({...devices['iPhone 13'], viewport: {width: 393, height: 800}});
  const p = await c.newPage();
  const foto = (n) => p.screenshot({path: `${SALIDA}/${n}.png`});
  await p.goto(`${URL}/capturar`); await foto('1-perfil');
  await p.click('.perfil >> nth=2'); await foto('2-nueva');
  // «Analizando» dura muy poco; se fuerza para la captura.
  await p.evaluate(() => { for (const id of ['forma-captura', 'sesion']) document.getElementById(id).hidden = true;
    document.getElementById('analizando').hidden = false; });
  await foto('3-analizando');
  await p.goto(`${URL}/capturar`);
  const nav = p.waitForURL(/inspeccionar/, {timeout: 60000}); await p.setInputFiles('#foto', FOTO); await nav;
  await p.waitForFunction(() => document.getElementById('n-revisar').textContent !== '…', null, {timeout: 60000});
  await p.waitForTimeout(1500); await foto('4-inspeccion');
  // Acepta las sugerencias y corrige una, para que el cierre muestre «1 corregida».
  for (let i = 0; i < 40; i++) {
    if (await p.locator('#terminada').isVisible()) break;
    const sug = await p.evaluate(() => document.querySelector('#detalle b').textContent);
    if (i === 2) await p.click('.clases button >> nth=0');
    else await p.locator('.clases button', {hasText: sug}).first().click();
    await p.waitForTimeout(80);
    if (i === 4) {
      await p.evaluate(() => { document.getElementById('titulo-union').scrollIntoView({block: 'start'}); window.scrollBy(0, -260); });
      await p.waitForTimeout(300); await foto('5-revision');
    }
  }
  await p.evaluate(() => document.getElementById('terminada').scrollIntoView({block: 'center'}));
  await p.waitForTimeout(300); await foto('6-terminada');
  await b.close();
})();
