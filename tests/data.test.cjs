const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
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