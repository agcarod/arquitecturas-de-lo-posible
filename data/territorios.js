/*
  Indicadores territoriales de contexto (DANE ECV/FIES 2023–2025).
  No representan la muestra de jóvenes de 18–28 años ni posibilidades individuales.
  Ver metodologia.html y docs/FUENTES_Y_METODO.md para denominadores y límites.
*/
window.PUERTAS_DATA = Object.freeze({
  publication: "26 de noviembre de 2026",
  territories: [
    {
      id:"choco",name:"Chocó",tag:"Pacífico",insight:"La inseguridad alimentaria de los hogares aumentó 20,5 puntos porcentuales entre 2024 y 2025.",
      metrics:{food2023:18.9,internet:36.4,food:56.8,foodPrevious:36.3,education:45.6}
    },
    {
      id:"guajira",name:"La Guajira",tag:"Caribe",insight:"Los hogares combinan inseguridad alimentaria con conectividad superior a la de Chocó.",
      metrics:{food2023:50.1,internet:52.6,food:47.8,foodPrevious:52.4,education:47.9}
    },
    {
      id:"bogota",name:"Bogotá D. C.",tag:"Capital",insight:"La mayor conectividad y asistencia educativa entre estos cuatro territorios coexisten con hogares que también enfrentan inseguridad alimentaria.",
      metrics:{food2023:21.2,internet:82.9,food:9.6,foodPrevious:13.9,education:60.7}
    },
    {
      id:"vaupes",name:"Vaupés",tag:"Amazonía",insight:"La baja conectividad y la reducción de inseguridad alimentaria son condiciones distintas y no deben agregarse en un puntaje único.",
      metrics:{food2023:34.4,internet:18.6,food:22.3,foodPrevious:46.1,education:39.6}
    }
  ],
  sources: {
    connectivity:"https://www.dane.gov.co/files/operaciones/ECV/bol-ECV-2025.pdf#page=12",
    education:"https://www.dane.gov.co/files/operaciones/ECV/bol-ECV-2025.pdf#page=19",
    food:"https://www.dane.gov.co/files/operaciones/FIES/bol-FIES-2025.pdf#page=6",
    victims:"https://datospaz.unidadvictimas.gov.co/registro-unico-de-victimas/"
  }
});