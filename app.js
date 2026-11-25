'use strict';
(() => {
  const app = window.PUERTAS_DATA;
  if (!app) throw new Error('No se encontró data/territorios.js');
  const $ = id => document.getElementById(id);
  const territories = app.territories;
  const fmtN = number => Number(number).toLocaleString('es-CO');
  const fmtP = number => Number(number).toLocaleString('es-CO', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
  const byId = id => territories.find(item => item.id === id);
  const state = { territory: 'choco', compare: 'bogota' };
  const colors = { choco: '#e0bb85', guajira: '#c4e7ae', bogota: '#7bc9ca', vaupes: '#d69aad' };

  function getComparison(value, other, name) {
    const difference = Math.round((value - other) * 10) / 10;
    if (difference === 0) return `Mismo valor publicado que ${name}.`;
    return `${fmtP(Math.abs(difference))} puntos porcentuales ${difference > 0 ? 'más' : 'menos'} que ${name}.`;
  }
  function setMetric(name, value, other, compareName) {
    $(`${name}-val`).textContent = fmtP(value);
    $(`${name}-meter`).style.width = Math.min(100, Math.max(0, value)) + '%';
    $(`${name}-compare`).textContent = getComparison(value, other, compareName);
  }
  function displayTerritory() {
    const current = byId(state.territory), other = byId(state.compare);
    $('population-total').textContent = fmtN(current.population.all);
    $('population-place').textContent = current.name;
    $('population-source').href = current.sources.population;
    $('pop-children').textContent = fmtN(current.population.child);
    $('pop-adolescent').textContent = fmtN(current.population.adolescent);
    $('population-child-share').style.width = (100 * current.population.child / current.population.all).toFixed(2) + '%';
    setMetric('internet', current.metrics.internet, other.metrics.internet, other.name);
    setMetric('food', current.metrics.food, other.metrics.food, other.name);
    setMetric('education', current.metrics.education, other.metrics.education, other.name);
    $('territory-insight').textContent = current.insight;
    $('comparison-reading').textContent = `La lectura de ${current.name} frente a ${other.name} depende del indicador elegido y de su población de referencia. No existe una suma válida de «oportunidades buenas» y «malas».`;
    const bars = [
      { label: 'Internet', field: 'internet', color: '#278f7f' },
      { label: 'Alimentación', field: 'food', color: '#d2a36f' },
      { label: 'Educación', field: 'education', color: '#799ca8' }
    ];
    const root = $('side-compare');
    root.replaceChildren();
    for (const indicator of bars) {
      const label = document.createElement('div');
      label.className = 'kind'; label.textContent = indicator.label;
      const barbox = document.createElement('div'); barbox.className = 'barbox';
      const bar = document.createElement('div'); bar.className = 'bar';
      bar.style.width = current.metrics[indicator.field] + '%';bar.style.background = indicator.color;
      barbox.append(bar);
      const value = document.createElement('div'); value.className = 'value';
      value.textContent = `${fmtP(current.metrics[indicator.field])}%`;
      const row = document.createElement('div'); row.className = 'side-row';
      row.append(label,barbox,value);root.append(row);
    }
    updateTrendText(current);
    renderTrend();
  }
  function changeTerritory(next) {
    if (!byId(next)) return;
    state.territory=next;
    if (state.compare === next) state.compare=territories.find(t=>t.id !== next).id;
    $('territory').value=state.territory;
    $('compare').value=state.compare;
    displayTerritory();
  }
  $('territory').addEventListener('change', e => changeTerritory(e.target.value));
  $('compare').addEventListener('change', e => {
    state.compare=e.target.value;
    if (state.compare===state.territory) state.compare=territories.find(t=>t.id!==state.territory).id;
    $('compare').value=state.compare;displayTerritory();
  });
  function updateTrendText(t) {
    const d=Math.round((t.metrics.food-t.metrics.foodPrevious)*10)/10;
    $('trend-name').textContent=t.name;
    $('trend-delta').textContent=(d>0?'+':'')+fmtP(d)+' p.p. (2024–2025)';
    $('trend-delta').style.color=d>0?'#f4be8d':'#c5e9ae';
    $('trend-statement').textContent=`Serie 2023–2025: ${fmtP(t.metrics.food2023)}%, ${fmtP(t.metrics.foodPrevious)}% y ${fmtP(t.metrics.food)}% de hogares. DANE señala un cambio significativo entre 2024 y 2025, pero no demuestra una tendencia sostenida ni sus causas.`;
  }
  function renderTrend() {
    const root=$('trend-chart');
    const ns='http://www.w3.org/2000/svg';
    const svg=document.createElementNS(ns,'svg');
    svg.setAttribute('viewBox','0 0 710 285');
    svg.setAttribute('role','img');
    svg.setAttribute('aria-label','Serie de inseguridad alimentaria 2023, 2024 y 2025 para Chocó, La Guajira, Bogotá y Vaupés (DANE)');
    const add=(name,attrs,content)=>{const e=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))e.setAttribute(k,String(v));if(content!==undefined)e.textContent=content;svg.append(e);return e;};
    const xs=[95,350,610],y0=229,yTo=v=>y0-(v/60)*185;
    [0,20,40,60].forEach(n=>{const y=yTo(n);add('line',{x1:xs[0],y1:y,x2:xs[2],y2:y,stroke:'#4d7575','stroke-dasharray':'4 6','stroke-width':1});add('text',{x:68,y:y+4,fill:'#b2cac6','font-size':12,'text-anchor':'end'},n+'%');});
    [2023,2024,2025].forEach((year,i)=>add('text',{x:xs[i],y:262,fill:'#dbece7','font-size':14,'font-weight':700,'text-anchor':'middle'},year));
    const ordered=[...territories].sort((a,b)=>Number(a.id===state.territory)-Number(b.id===state.territory));
    ordered.forEach(t=>{
      const active=t.id===state.territory;
      const ys=[t.metrics.food2023,t.metrics.foodPrevious,t.metrics.food].map(yTo);
      add('path',{d:`M ${xs[0]} ${ys[0]} L ${xs[1]} ${ys[1]} L ${xs[2]} ${ys[2]}`,stroke:colors[t.id],'stroke-width':active?4.7:2.5,opacity:active?1:.5,fill:'none','stroke-linejoin':'round','stroke-linecap':'round'});
      xs.forEach((x,i)=>add('circle',{cx:x,cy:ys[i],r:active?5:3.3,stroke:'#143f42','stroke-width':1.3,fill:colors[t.id],opacity:active?1:.68}));
      if(active)add('text',{x:xs[2]+12,y:ys[2]-9,fill:'#ffffff','font-size':14,'font-weight':800},`${fmtP(t.metrics.food)}%`);
    });
    root.replaceChildren(svg);
    const legend=$('trend-legend');legend.replaceChildren();
    territories.forEach(t=>{const b=document.createElement('button');b.type='button';b.className='legend-button'+(t.id===state.territory?' current':'');b.setAttribute('aria-label','Mostrar '+t.name);const circle=document.createElement('span');circle.className='legend-circle';circle.style.background=colors[t.id];const label=document.createElement('span');label.textContent=t.name;b.append(circle,label);b.addEventListener('click',()=>changeTerritory(t.id));legend.append(b);});
  }
  const topics={
    internet:{label:'conectividad',question:'¿En qué condiciones la conexión disponible se convierte en oportunidades efectivas de aprendizaje, información y participación?',need:'Acceso individual, calidad de conexión, dispositivos, costos y capacidades de uso; indicadores actuales son de hogares.',study:'Encuestas a hogares + cartografía de acceso + comparación de establecimientos y territorios; seguimiento de uso efectivo.',challenge:'El aumento de conectividad no cambia la participación una vez consideradas las condiciones educativas y familiares.'},
    food:{label:'seguridad alimentaria',question:'¿Cómo se relacionan las privaciones alimentarias del hogar con las posibilidades educativas y de cuidado de niñas, niños y adolescentes?',need:'Microdatos adecuados o información individual sobre alimentación, asistencia, experiencias escolares y apoyos institucionales.',study:'Análisis multinivel con medidas vinculadas de hogares, escuelas y territorio; evaluación de factores de confusión y temporalidad.',challenge:'Las asociaciones se atenúan o revierten al incorporar ingresos, shocks familiares, apoyos y selección.'},
    education:{label:'continuidad educativa',question:'¿Qué condiciones convierten la oferta educativa en posibilidades reales de continuidad, y quiénes quedan fuera de ese recorrido?',need:'Datos longitudinales sobre asistencia, interrupciones, transporte, costos, barreras administrativas y trayectorias educativas.',study:'Análisis por curso de vida con secuencias longitudinales, entrevistas de trayectorias e indicadores territoriales.',challenge:'Los indicadores de oferta y acceso no explican diferencias cuando se evalúan costos de oportunidad, condiciones familiares y transiciones.'},
    violence:{label:'violencia y protección',question:'¿Cómo interactúan la exposición a violencia, las redes comunitarias y las capacidades institucionales en las trayectorias de niñas, niños y adolescentes?',need:'Hechos victimizantes desagregados por edad, lugar, período y registro; información sobre redes de protección y acceso a servicios.',study:'Primero auditabilidad y calidad de registros RUV; después triangulación con evidencia cualitativa y otras fuentes territoriales.',challenge:'Los patrones se explican principalmente por diferencias de registro y accesibilidad institucional, no por exposición real comparable.'}
  };
  const lenses={
    institution:{name:'instituciones',modifier:'reglas, recursos y barreras institucionales'},
    networks:{name:'redes de cuidado',modifier:'apoyos y relaciones comunitarias'},
    trajectory:{name:'curso de vida',modifier:'acumulación de experiencias y cambios en el tiempo'}
  };
  let questionText='';
  function updateQuestion(){
    const t=topics[$('barrier').value],lens=lenses[$('mechanism').value];
    const selected=byId(state.territory);
    $('research-question').textContent=t.question;
    $('missing-data').textContent=t.need;
    $('study-design').textContent=`${t.study} Perspectiva seleccionada: ${lens.modifier}.`;
    $('falsification').textContent=t.challenge;
    questionText=`¿CUÁNTAS PUERTAS SE ABREN DONDE CRECES? — FICHA EXPLORATORIA DE PREGUNTA Y DISEÑO
Territorio de referencia: ${selected.name}
Tema: ${t.label}
Perspectiva: ${lens.name}

PREGUNTA
${t.question}

INFORMACIÓN QUE FALTA
${t.need}

DISEÑO INICIAL
${t.study}
Perspectiva: ${lens.modifier}

CRITERIO DE REFUTACIÓN
${t.challenge}

NOTAS
Ejercicio metodológico ilustrativo: no es un protocolo aprobado, una evaluación causal ni el diseño empírico longitudinal de la propuesta posdoctoral.
Fuentes y método: metodologia.html
`;
  }
  $('barrier').addEventListener('change',updateQuestion);$('mechanism').addEventListener('change',updateQuestion);
  function download(name,text){const blob=new Blob([text],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);}
  $('copy-question').addEventListener('click',async()=>{
    const status=$('copy-status');
    try { if(!navigator.clipboard||!navigator.clipboard.writeText)throw new Error('Sin acceso al portapapeles');await navigator.clipboard.writeText(questionText);status.textContent='Pregunta copiada al portapapeles.';}
    catch { download('pregunta_de_investigacion.txt',questionText);status.textContent='El navegador descargó la ficha en TXT.'; }
  });
  // Nota: cada cambio de territorio también actualiza la ficha con el territorio de referencia.
  const old=displayTerritory;
  displayTerritory=function(){old();updateQuestion();};
  $('territory').value=state.territory;$('compare').value=state.compare;
  displayTerritory();
})();

// La ECV se carga desde un archivo agregado reproducible. La tabla HTML sigue
// disponible como alternativa si la petición o JavaScript no están activos.
(async function () {
  const byId = id => document.getElementById(id);
  const fmt = (value, digits = 2) => Number(value).toLocaleString("es-CO", {
    minimumFractionDigits: digits, maximumFractionDigits: digits
  });
  const groupSelect = byId("group-select");
  if (groupSelect) {
    try {
      const response = await fetch("data/ecv2025_summary.json");
      if (!response.ok) throw new Error("No se pudo cargar el agregado ECV");
      const summary = await response.json();
      const groupMap = new Map(summary.groups.map(group => [group.id, group]));
      function showGroup(id) {
        const group = groupMap.get(id);
        if (!group) return;
        byId("group-share").textContent = fmt(group.weighted_share_pct) + " %";
        byId("group-n").textContent = "n = " + Number(group.sample_n).toLocaleString("es-CO");
        byId("group-life").textContent = fmt(group.outcomes.life_satisfaction.estimate);
        byId("group-meaning").textContent = fmt(group.outcomes.activities_worthwhile.estimate);
        byId("group-time").textContent = fmt(group.outcomes.free_time_satisfaction.estimate);
        byId("group-income").textContent = fmt(group.outcomes.household_income_reaches_minimum.estimate) + " %";
        byId("group-definition").textContent = group.definition + " Participación ponderada: " + fmt(group.weighted_share_pct) + " %.";
      }
      groupSelect.addEventListener("change", () => showGroup(groupSelect.value));
      showGroup(groupSelect.value);

      const chart = byId("config-plot");
      if (chart) {
        chart.replaceChildren();
        for (const group of summary.groups) {
          const row = document.createElement("div");
          row.className = "config-bar-row";
          const label = document.createElement("span");
          label.className = "config-bar-label";
          label.textContent = group.name;
          const track = document.createElement("span");
          track.className = "config-bar-track";
          const bar = document.createElement("span");
          bar.className = "config-bar-fill";
          bar.style.width = group.weighted_share_pct + "%";
          bar.setAttribute("aria-hidden", "true");
          track.append(bar);
          const value = document.createElement("strong");
          value.className = "config-bar-value";
          value.textContent = fmt(group.weighted_share_pct) + " %";
          row.append(label, track, value);
          chart.append(row);
        }
      }
    } catch (error) {
      console.warn("Los datos agregados ECV no se cargaron; queda visible la tabla estática.", error);
    }
  }

  const rules = window.ARCHITECTURES_RULES;
  const option = byId("life-option");
  if (!rules || !option) return;

  const labels = {
    C: "Compatible/documentado",
    R: "Restricción documentada",
    U: "Indeterminado"
  };
  const lifeLabels = {
    C: "Compatible en este ejemplo",
    R: "Restricción documentada",
    U: "No se puede concluir todavía"
  };
  const expansionLabels = {
    C: "Candidata a estudio",
    R: "Requiere rediseño",
    U: "Indeterminada"
  };
  function displayDemo() {
    const result = rules.evaluate({
      economy: byId("economy-state").value,
      institution: byId("institution-state").value,
      time: byId("time-state").value,
      continuity: byId("continuity-state").value,
      family: byId("family-state").value,
      externalCost: byId("cost-state").value,
      rights: byId("rights-state").value,
      equity: byId("equity-state").value
    });
    byId("demo-option").textContent = option.options[option.selectedIndex].text;
    for (const [id, state] of [
      ["demo-access", result.accessibility],
      ["demo-compatible", result.compatibility],
      ["demo-sustain", result.sustainability]
    ]) {
      const el = byId(id);
      el.textContent = labels[state];
      el.dataset.state = state;
    }
    const overall = byId("demo-overall");
    overall.textContent = lifeLabels[result.life];
    overall.dataset.state = result.life;
    const expand = byId("demo-expand");
    expand.textContent = expansionLabels[result.expansion];
    expand.dataset.state = result.expansion;
    const explanation = byId("demo-explanation");
    if (result.life === "R") {
      explanation.textContent = "Al menos un requisito listado aparece restringido. El ejemplo invita a registrar cuál, para quién y en qué momento; no estima la probabilidad de realizar la alternativa.";
    } else if (result.life === "U") {
      explanation.textContent = "Falta información para evaluar uno o más requisitos. Indeterminación no significa imposibilidad.";
    } else {
      explanation.textContent = "Los requisitos incluidos aparecen compatibles en este caso hipotético. Las condiciones omitidas, la valoración personal y los cambios futuros siguen sin evaluarse.";
    }
    explanation.dataset.state = result.life;
  }
  for (const id of [
    "life-option", "economy-state", "institution-state", "time-state",
    "continuity-state", "family-state", "cost-state", "rights-state", "equity-state"
  ]) byId(id).addEventListener("change", displayDemo);
  displayDemo();
})();
