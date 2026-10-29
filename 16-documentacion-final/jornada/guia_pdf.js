// Regenera guia-raspberry-pi.pdf desde guia-raspberry-pi.md (pandoc + Playwright).
// Desde la raíz del repositorio:
//   sed '1,/^---$/{/^---$/!d};1,/^---$/d' 16-documentacion-final/jornada/guia-raspberry-pi.md \
//     | pandoc -s --css guia.css --metadata title="Guía de la jornada" -o 16-documentacion-final/jornada/guia.html
//   node 16-documentacion-final/jornada/guia_pdf.js
// (el sed quita el frontmatter; si pandoc no lo quita bien, borrarlo a mano en una copia).
const path = require('path');
const {chromium} = require('playwright');
const dir = __dirname;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('file://' + path.join(dir, 'guia.html'));
  await p.pdf({path: path.join(dir, 'guia-raspberry-pi.pdf'), format: 'Letter', printBackground: true,
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8pt;width:100%;text-align:center;font-family:Arial;color:#3b2f3f">Guía de la jornada, página <span class="pageNumber"></span> de <span class="totalPages"></span></div>',
    margin: {top: '16mm', bottom: '18mm', left: '16mm', right: '16mm'}});
  await b.close();
})();
