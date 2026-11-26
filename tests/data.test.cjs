const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const summary = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'ecv2025_summary.json'),'utf8'));
const sexSummary = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'data', 'ecv2025_sex.json'),'utf8'));
const source = fs.readFileSync(path.join(__dirname, '..', 'data', 'territorios.js'),'utf8');
const context={window:{}};
vm.runInNewContext(source,context);
const all=context.window.PUERTAS_DATA.territories;

test('Hay cuatro territorios identificados, sin IDs repetidos',()=>{
  assert.equal(all.length,4);
  assert.equal(new Set(all.map(t=>t.id)).size,4);
});
test('El atlas excluye recuentos secundarios que no corresponden a la muestra',()=>{
  for (const t of all) assert.ok(!('population' in t),t.name);
  assert.ok(!source.includes('telencuestas.com'));
});
test('Indicadores válidos en su propia escala',()=>{
  for (const t of all) {
    for(const [key,val] of Object.entries(t.metrics)){
      assert.ok(typeof val==='number' && Number.isFinite(val) && val>=0 && val<=100,`${t.name}: ${key}`);
    }
    assert.equal(t.metrics.food2023 !== undefined,true);
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
test('El hallazgo preliminar abre la portada y queda separado del atlas contextual',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  const hero=html.indexOf('id="inicio"'), finding=html.indexOf('id="hallazgo"'), atlas=html.indexOf('id="atlas"');
  assert.ok(hero>=0 && hero<finding && finding<atlas);
  assert.ok(html.includes('8,28'));
  assert.ok(html.includes('8,18'));
  assert.ok(html.includes('69,6'));
  assert.ok(html.includes('53,1'));
  assert.ok(html.includes('16,5 puntos porcentuales'));
  assert.ok(html.includes('¿Cómo podemos construir las condiciones del bienestar futuro'));
  assert.ok(html.includes('¿Qué formas de vida permiten a las juventudes experimentar bienestar'));
  assert.ok(html.includes('Atlas de contexto territorial, distinto de la población del estudio'));
  assert.ok(!html.includes('telencuestas.com'));
});
test('La carta y el sitio comparten el diseño del piloto del año 1',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  const method=fs.readFileSync(path.join(__dirname,'..','metodologia.html'),'utf8');
  for (const text of ['6–8 jóvenes','dos encuentros separados por seis a ocho semanas','juicios prospectivos','antes de conocer el seguimiento'])
    assert.ok(method.includes(text),text);
  assert.ok(html.includes('dos encuentros separados por seis a ocho semanas'));
  assert.ok(html.includes('AÑO 3 · INTEGRAR Y FORMULAR ALTERNATIVAS'));
  assert.ok(!html.includes('entrevistas cognitivas'));
  assert.ok(!html.includes('AÑO 3 · CONTRASTAR Y REVISAR'));
  assert.ok(!html.includes('En el año 3 se propone una comparación contrabalanceada'));
  assert.ok(method.includes('Durante el piloto del año 1 se compararán dos análisis independientes'));
});
test('La portada ya no publica el generador ni presenta el test lógico como evidencia',()=>{
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  assert.ok(!html.includes('id="preguntas"'));
  assert.ok(!html.includes('id="copy-question"'));
  assert.ok(!html.includes('PRUEBA LÓGICA EJECUTADA'));
  assert.ok(!html.includes('10 de 10 casos sintéticos'));
  assert.ok(!html.includes('27 de 27 combinaciones'));
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

test('La composición ponderada por sexo al nacer coincide con los cinco módulos',()=>{
  const work=sexSummary.sex_at_birth.groups.find(g=>g.id==='occupied_no_study');
  const home=sexSummary.sex_at_birth.groups.find(g=>g.id==='home_primary');
  assert.equal(sexSummary.sex_at_birth.variable,'P6020');
  assert.equal(work.sample_n,18189);
  assert.equal(home.sample_n,7205);
  assert.equal(work.sample_n_women,6877);
  assert.equal(work.sample_n_men,11312);
  assert.equal(home.sample_n_women,6514);
  assert.equal(home.sample_n_men,691);
  assert.ok(Math.abs(work.weighted_sex_at_birth_pct.women_P6020_2-39.2)<0.1);
  assert.ok(Math.abs(work.weighted_sex_at_birth_pct.men_P6020_1-60.8)<0.1);
  assert.ok(Math.abs(home.weighted_sex_at_birth_pct.women_P6020_2-90.4)<0.1);
  assert.ok(Math.abs(home.weighted_sex_at_birth_pct.men_P6020_1-9.6)<0.1);
  assert.equal(sexSummary.sex_at_birth.label,'sexo al nacer (no identidad de género)');
});

test('El selector ofrece total, mujeres y hombres con seis categorías y resultados separados',()=>{
  assert.deepEqual(Object.keys(sexSummary.views),['all','women','men']);
  for(const view of Object.values(sexSummary.views)){
    assert.equal(view.length,6);
    assert.ok(view.every(g=>typeof g.sample_n==='number'));
  }
  const html=fs.readFileSync(path.join(__dirname,'..','index.html'),'utf8');
  for(const token of ['id="sex-view-select"','value="all"','value="women"','value="men"','id="sex-composition-chart"','id="sex-outcome-panels"']) assert.ok(html.includes(token),token);
  assert.ok(sexSummary.minimum_unweighted_n_for_interactive_outcomes===50);
});

test('La sensibilidad restringida a mujeres reproduce estimaciones e intervalos aproximados',()=>{
  const s=sexSummary.women_only_age_standardized_sensitivity;
  assert.deepEqual(s.sample_n,{occupied_no_study:6877,home_primary:6514});
  assert.ok(Math.abs(s.contrasts.income_sufficient.difference_occupied_minus_home-17.24)<0.01);
  assert.ok(Math.abs(s.contrasts.income_sufficient.ci95_approx[0]-14.24)<0.01);
  assert.ok(Math.abs(s.contrasts.income_sufficient.ci95_approx[1]-20.25)<0.01);
  assert.ok(Math.abs(s.contrasts.P1895.difference_occupied_minus_home-0.20)<0.01);
  assert.ok(Math.abs(s.contrasts.P1895.ci95_approx[0]-0.10)<0.01);
  assert.ok(Math.abs(s.contrasts.P1895.ci95_approx[1]-0.30)<0.01);
  assert.equal(s.estimates.occupied_no_study.P1895.estimate,8.3121);
  assert.equal(s.estimates.home_primary.income_sufficient.estimate,54.6411);
});

test('Los scripts y las salidas de reproducción por sexo están publicados localmente',()=>{
  for(const p of ['data/ecv2025_sex.json','data/ecv2025_sex_composition.csv','scripts/build_ecv2025_sex_dashboard.py','scripts/ECV2025_contraste_por_sexo.py','results/resultado_contraste_por_sexo.txt'])
    assert.ok(fs.existsSync(path.join(__dirname,'..',p)),p);
  const result=fs.readFileSync(path.join(__dirname,'..','results','resultado_contraste_por_sexo.txt'),'utf8');
  assert.ok(result.includes('subset 2'));
  assert.ok(result.includes('17.24150029'));
});
