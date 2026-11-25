const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const summary = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'ecv2025_summary.json'),'utf8'));
const source = fs.readFileSync(path.join(__dirname, '..', 'data', 'territorios.js'),'utf8');
const context={window:{}};
vm.runInNewContext(source,context);
const all=context.window.PUERTAS_DATA.territories;

test('Hay cuatro territorios identificados, sin IDs repetidos',()=>{
  assert.equal(all.length,4);
  assert.equal(new Set(all.map(t=>t.id)).size,4);
});
test('La población total coincide con el desglose por edad',()=>{
  for (const t of all) {
    assert.equal(t.population.all,t.population.child+t.population.adolescent,t.name);
    assert.equal(t.population.year,2025,t.name);
  }
});
test('Indicadores válidos en su propia escala',()=>{
  for (const t of all) {
    for(const [key,val] of Object.entries(t.metrics)){
      assert.ok(typeof val==='number' && Number.isFinite(val) && val>=0 && val<=100,`${t.name}: ${key}`);
    }
    assert.ok(t.sources.population.startsWith('https://'));
  }
});
test('Valores de contraste territorial reproducen el boletín',()=>{
  const choco=all.find(t=>t.id==='choco');const vaupes=all.find(t=>t.id==='vaupes');
  assert.equal(Math.round((choco.metrics.food-choco.metrics.foodPrevious)*10)/10,20.5);
  assert.equal(Math.round((vaupes.metrics.food-vaupes.metrics.foodPrevious)*10)/10,-23.8);
});
test('Archivos necesarios para GitHub Pages están presentes',()=>{
  for(const p of ['index.html','styles.css','app.js','.nojekyll','README.md','docs/FUENTES_Y_METODO.md','data/indicadores_2025.csv','assets/favicon.svg']){
    assert.ok(fs.existsSync(path.join(__dirname,'..',p)),p);
  }
});

test('La atribución y el contexto posdoctoral aparecen en la portada',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  assert.ok(html.includes('Ángela Gissette Caro-Delgado'));
  assert.ok(html.includes('Futuros de las Ciencias Sociales'));
  assert.ok(html.includes('no constituye un proyecto institucional aprobado'));
});
test('Serie FIES 2023-2025 cotejada con dos boletines DANE',()=>{const expected={choco:18.9,guajira:50.1,bogota:21.2,vaupes:34.4};for(const v of all)assert.equal(v.metrics.food2023,expected[v.id]);});
test('Tabla estática, metodología legible y enlace de publicar eliminado',()=>{const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');assert.ok(html.includes('<table class="fallback-table">'));assert.ok(html.includes('metodologia.html'));assert.ok(!html.includes('https://github.com/new'));assert.ok(fs.existsSync(path.join(__dirname,'..','metodologia.html')));});

test('El laboratorio presenta las cinco secciones solicitadas',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  for(const id of ['atlas','vidas','renuncias','protocolo','agenda']) assert.ok(html.includes(`id="${id}"`),id);
  assert.ok(html.includes('¿Cuántas puertas se abren donde creces?'));
  assert.ok(html.includes('¿Experimentar bienestar significa disponer de las mismas condiciones'));
});
test('El resumen ECV conserva la base, hogares y seis categorías',()=>{
  assert.equal(summary.person_records,35776);
  assert.equal(summary.households,27632);
  assert.equal(summary.modules_integrated,5);
  assert.equal(summary.records_lost,0);
  assert.equal(summary.groups.length,6);
  assert.equal(summary.groups.reduce((n,g)=>n+g.sample_n,0),35776);
  assert.equal(summary.groups.find(g=>g.id==='home_primary').sample_n,7205);
  assert.ok(Math.abs(summary.groups.reduce((n,g)=>n+g.weighted_share_pct,0)-100)<0.02);
});
test('El contraste reproducible conserva la sensibilidad a umbrales',()=>{
  const s=summary.standardized_contrasts;
  assert.deepEqual(s.life_satisfaction.ci95_approx,[-0.257,0.048]);
  assert.deepEqual(s.household_income_reaches_minimum.ci95_approx,[-20.758,-12.141]);
  assert.deepEqual(summary.joint_threshold_sensitivity.map(x=>x.threshold),[7,8,9]);
  assert.ok(summary.joint_threshold_sensitivity[2].ci95_approx_pp[0]<0);
  assert.ok(summary.joint_threshold_sensitivity[2].ci95_approx_pp[1]>0);
});
test('Reglas interactivas C/R/U respetan restricciones e indeterminación',()=>{
  const source=fs.readFileSync(path.join(__dirname,'..','data','demo_logic.js'),'utf8');
  const context={window:{}};vm.runInNewContext(source,context);
  const rules=context.window.ARCHITECTURES_RULES;
  assert.equal(rules.stateOf([]),'U');
  assert.equal(rules.stateOf(['C','R','U']),'R');
  const allC=rules.evaluate({economy:'C',institution:'C',family:'C',time:'C',continuity:'C',equity:'C',externalCost:'C',rights:'C'});
  assert.deepEqual(JSON.parse(JSON.stringify(allC)),{accessibility:'C',compatibility:'C',sustainability:'C',life:'C',expansion:'C'});
  const missing=rules.evaluate({economy:'C',institution:'U',family:'C',time:'C',continuity:'C',equity:'C',externalCost:'C',rights:'C'});
  assert.equal(missing.life,'U');
  const blocked=rules.evaluate({economy:'R',institution:'C',family:'C',time:'C',continuity:'C',equity:'R',externalCost:'C',rights:'C'});
  assert.equal(blocked.life,'R');
  assert.equal(blocked.expansion,'R');
});
test('Las descargas agregadas y los scripts públicos existen; no hay ZIP de microdatos',()=>{
  for(const p of ['data/ecv2025_summary.json','data/ecv2025_groups.csv','data/demo_logic.js','scripts/build_ecv2025_dashboard.py','scripts/prueba_robustez_ecv.py','scripts/prueba_logica_arquitecturas.py','results/resultado_robustez_ecv.txt','results/resultado_prueba_logica.txt'])
    assert.ok(fs.existsSync(path.join(__dirname,'..',p)),p);
  const files=fs.readdirSync(path.join(__dirname,'..'),{withFileTypes:true});
  assert.ok(!files.some(f=>f.isFile()&&f.name.endsWith('.zip')));
});
test('Todos los enlaces y recursos locales de las dos páginas apuntan a archivos existentes',()=>{
  for(const pageName of ['index.html','metodologia.html']){
    const html=fs.readFileSync(path.join(__dirname,'..',pageName),'utf8');
    for(const match of html.matchAll(/(?:href|src)="([^"]+)"/g)){
      const raw=match[1];
      if(/^(?:https?:|mailto:|tel:|data:|javascript:|#)/i.test(raw)) continue;
      const target=decodeURIComponent(raw.split(/[?#]/)[0]);
      if(!target) continue;
      const resolved=path.resolve(__dirname,'..',path.dirname(pageName),target);
      assert.ok(fs.existsSync(resolved),`${pageName}: ${raw}`);
    }
  }
});
