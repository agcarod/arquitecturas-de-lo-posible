/*
  Fuente demográfica: cifras publicadas por Telencuestas que atribuye a DANE. No cotejadas con el libro oficial vigente de DANE.
  Indicadores de contexto: DANE ECV 2025; FIES DANE 2023/2024/2025.
  Estas cifras NO provienen de una muestra de los mismos niños y jóvenes.
  Ver metodologia.html y docs/FUENTES_Y_METODO.md para denominadores, enlaces y páginas.
*/
window.PUERTAS_DATA = Object.freeze({
  publication: "12 de noviembre de 2026",
  territories: [
    {
      id:"choco",name:"Chocó",tag:"Pacífico",insight:"Una transformación acelerada de las condiciones materiales: la inseguridad alimentaria de los hogares aumentó 20,5 puntos porcentuales entre 2024 y 2025.",
      population:{all:231253,child:154346,adolescent:76907,year:2025},
      metrics:{food2023:18.9, internet:36.4, food:56.8,foodPrevious:36.3, education:45.6},
      sources:{population:"https://telencuestas.com/censos-de-poblacion/colombia/2025/choco"}
    },
    {
      id:"guajira",name:"La Guajira",tag:"Caribe",insight:"Las condiciones del territorio combinan una proporción considerable de hogares con inseguridad alimentaria y niveles de conectividad superiores a los de Chocó.",
      population:{all:417131,child:276983,adolescent:140148,year:2025},
      metrics:{food2023:50.1, internet:52.6,food:47.8,foodPrevious:52.4,education:47.9},
      sources:{population:"https://telencuestas.com/censos-de-poblacion/colombia/2025/la-guajira"}
    },
    {
      id:"bogota",name:"Bogotá D. C.",tag:"Capital",insight:"La mayor conectividad y asistencia educativa entre estos cuatro territorios coexisten con hogares que también enfrentan inseguridad alimentaria.",
      population:{all:1741825,child:1101730,adolescent:640095,year:2025},
      metrics:{food2023:21.2, internet:82.9,food:9.6,foodPrevious:13.9,education:60.7},
      sources:{population:"https://telencuestas.com/censos-de-poblacion/colombia/2025/bogota/bogota"}
    },
    {
      id:"vaupes",name:"Vaupés",tag:"Amazonía",insight:"La baja conectividad de los hogares y la importante reducción de la inseguridad alimentaria son señales distintas que no deben agregarse en un puntaje único.",
      population:{all:21997,child:14397,adolescent:7600,year:2025},
      metrics:{food2023:34.4, internet:18.6,food:22.3,foodPrevious:46.1,education:39.6},
      sources:{population:"https://telencuestas.com/censos-de-poblacion/colombia/2025/vaupes"}
    }
  ],
  sources: {
    connectivity:"https://www.dane.gov.co/files/operaciones/ECV/bol-ECV-2025.pdf",
    education:"https://www.dane.gov.co/files/operaciones/ECV/bol-ECV-2025.pdf",
    food:"https://www.dane.gov.co/files/operaciones/FIES/bol-FIES-2025.pdf",
    projections:"https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion",
    icbf:"https://portalsuin.icbf.gov.co/sites/suin/Pages/poblacion_ni%C3%B1os_ni%C3%B1as_Colombia.aspx",
    victims:"https://datospaz.unidadvictimas.gov.co/registro-unico-de-victimas/"
  }
});