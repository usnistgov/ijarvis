// class for the table initial display is none
//const tableStyle = document.getElementById("table-sort");
//tableStyle.classList.add("myTableStyle");
//tableStyle.style.display = "none";

//const tableStyle2 = document.getElementById("table-sort2");
//tableStyle.classList.add("myTableStyle");
//tableStyle.style.display = "none";
//New Table Initial
// const newTable = document.getElementById("table-data");

//change display to flex after search button press

//const buttonEffect = document.getElementById("searchButton");
//display results text to flex
//const pTextDisplayEffect = document.getElementById("pText-display");

//apply display effect

//apply display effect
//buttonEffect.addEventListener("click", () => {
//  tableStyle.classList.remove("myTableStyle");
//  tableStyle.classList.add("tableSection");
//  newTable.style.display = "flex";
//  tableStyle.style.display = "flex";
//  pTextDisplayEffect.classList.add("output-results-texts-effect");
//});

// class for the table initial display is none
const tableStyle = document.getElementById("table-sort");
tableStyle.classList.add("myTableStyle");
tableStyle.style.display = "none";

//New Table Initial

//change display to flex after search button press
const buttonEffect = document.getElementById("searchButton");

//display results text to flex
const pTextDisplayEffect = document.getElementById("pText-display");

//apply display effect
buttonEffect.addEventListener("click", () => {
  tableStyle.classList.remove("myTableStyle");
  tableStyle.classList.add("tableSection");
  tableStyle.style.display = "flex";
  newTable.style.display = "flex";
  pTextDisplayEffect.classList.add("output-results-texts-effect");
});

//Display search buttons in periodic table
const periodicTable = document.getElementById("container");
const periodicSearchBar = document.getElementById("periodic-search");

periodicTable.addEventListener("mouseenter", (e) => {
  let x = e.offsetX;
  let y = e.offsetY;

  periodicSearchBar.style.display = "flex";
});

//Remove search on mouse leave
periodicTable.addEventListener("mouseleave", (e) => {
  periodicSearchBar.style.display = "none";
  tableStyle.classList.add("tableSection");

  let x = e.offsetX;
  let y = e.offsetY;

  if (x >= 696) {
    periodicSearchBar.style.display = "flex";
  } else if (y >= 687) {
    periodicSearchBar.style.display = "none";
  }
});
periodicSearchBar.addEventListener("click", () => {
  tableStyle.style.display = "flex";
  newTable.style.display = "flex";
  tableStyle.classList.add("tableSection");
  pTextDisplayEffect.classList.add("output-results-texts-effect");
});

//Re-arrange Tables
//Store Table data
const th = document.getElementsByClassName("theader");

//console.log(myTableRows);
//Slide events

//OPT bandgap
let sliderOpt_l = document.getElementById("opgtbox_l");
let sliderOpt = document.getElementById("opgtbox");

let sliderValueMin = document.getElementById("sliderValuesMin");
let sliderValue = document.getElementById("sliderValues");
// slider value to text
sliderValueMin.textContent = sliderOpt_l.value;
sliderValue.textContent = sliderOpt.value;
//activate slider values
// maximum
sliderOpt.oninput = function () {
  sliderValue.textContent = sliderOpt.value;
};
//minimum
sliderOpt_l.oninput = function () {
  sliderValueMin.innerHTML = sliderOpt_l.value;
};

//MBJ bandgap
let sliderOpt1_l = document.getElementById("mbjtbox_l");
let sliderOpt1 = document.getElementById("mbjgtbox");
let sliderValue1Min = document.getElementById("sliderValues1Min");
let sliderValue1 = document.getElementById("sliderValues1");

// slider value to text
sliderValue1Min.textContent = sliderOpt1_l.value;
sliderValue1.textContent = sliderOpt1.value;
//activate slider values
sliderOpt1.oninput = function () {
  sliderValue1Min.textContent = sliderOpt1_l.value;
  sliderValue1.textContent = sliderOpt1.value;
};

//HSE-bandgap
let sliderOpt2 = document.getElementById("hsegtbox");
let sliderValue2 = document.getElementById("sliderValues2");
// slider value to text
sliderValue2.textContent = sliderOpt2.value;
//activate slider values
sliderOpt2.oninput = function () {
  sliderValue2.textContent = sliderOpt2.value;
};

//KV bvgtbx
let sliderOpt3Min = document.getElementById("bvgtbx_l");
let sliderOpt3 = document.getElementById("bvgtbx");
let sliderValue3Min = document.getElementById("sliderValues3Min");
let sliderValue3 = document.getElementById("sliderValues3");
// slider value to text
sliderValue3Min.textContent = sliderOpt3Min.value;
sliderValue3.textContent = sliderOpt3.value;
//activate slider values
sliderOpt3.oninput = function () {
  sliderValue3Min.textContent = sliderOpt3Min.value;
  sliderValue3.textContent = sliderOpt3.value;
};

//GV
let sliderOpt4 = document.getElementById("gvgtbx");
let sliderValue4 = document.getElementById("sliderValues4");
// slider value to text
sliderValue4.textContent = sliderOpt4.value;
//activate slider values
sliderOpt4.oninput = function () {
  sliderValue4.textContent = sliderOpt4.value;
};

//FORMATION
let sliderOpt5 = document.getElementById("fgtbox");
let sliderValue5 = document.getElementById("sliderValues5");
// slider value to text
sliderValue5.textContent = sliderOpt5.value;
//activate slider values
sliderOpt5.oninput = function () {
  sliderValue5.textContent = sliderOpt5.value;
};

//Exfoliation
let sliderOpt6 = document.getElementById("exfgtbox");
let sliderValue6 = document.getElementById("sliderValues6");
// slider value to text
sliderValue6.textContent = sliderOpt6.value;
//activate slider values
sliderOpt6.oninput = function () {
  sliderValue6.textContent = sliderOpt6.value;
};

//SPILLAGE
let sliderOpt7 = document.getElementById("spillgtbox");
let sliderValue7 = document.getElementById("sliderValues7");
// slider value to text
sliderValue7.textContent = sliderOpt7.value;
//activate slider values
sliderOpt7.oninput = function () {
  sliderValue7.textContent = sliderOpt7.value;
};

//SLME
let sliderOpt8 = document.getElementById("slmegtbox");
let sliderValue8 = document.getElementById("sliderValues8");
// slider value to text
sliderValue8.textContent = sliderOpt8.value;
//activate slider values
sliderOpt8.oninput = function () {
  sliderValue8.textContent = sliderOpt8.value;
};

//MAGMOM
let sliderOpt9 = document.getElementById("maggtbox");
let sliderValue9 = document.getElementById("sliderValues9");
// slider value to text
sliderValue9.textContent = sliderOpt9.value;
//activate slider values
sliderOpt9.oninput = function () {
  sliderValue9.textContent = sliderOpt9.value;
};

//DENSITY
let sliderOpt10 = document.getElementById("densitygtbox");
let sliderValue10 = document.getElementById("sliderValues10");
// slider value to text
sliderValue10.textContent = sliderOpt10.value;
//activate slider values
sliderOpt10.oninput = function () {
  sliderValue10.textContent = sliderOpt10.value;
};

//SPG
let sliderOpt11 = document.getElementById("spggtbox");
let sliderValue11 = document.getElementById("sliderValues11");
// slider value to text
sliderValue11.textContent = sliderOpt11.value;
//activate slider values
sliderOpt11.oninput = function () {
  sliderValue11.textContent = sliderOpt11.value;
};

//nAtoms
let sliderOpt12 = document.getElementById("natsgtbox");
let sliderValue12 = document.getElementById("sliderValues12");
// slider value to text
sliderValue12.textContent = sliderOpt12.value;
//activate slider values
sliderOpt12.oninput = function () {
  sliderValue12.textContent = sliderOpt12.value;
};

// console.log(sliderValue12.textContent);

// //SLIDER EFFECTATION
// function sliderFilterer(x) {
//   let rowUpdateNow = tableStyle.rows;
//   let currentCellX,
//     currentCellY = 0;

//   //SKIP the first row!
//   for (let i = 1; i < rowUpdateNow.length; i++) {
//     for (let j = 0; j < rowUpdateNow[i].length; j++) {
//       //iterate through columns: if first column not in range: HIDE, else SHOW

//       // density column test
//       //get data in density column cell
//       currentCellX = rows[i].getElementsByTagName("TD")[n];
//       if (j == sliderOpt10) {
//         // check for interval
//         if (
//           currentCellX.textContent.toLowerCase() >= 0 &&
//           currentCellX.textContent.toLowerCase() <= sliderValue10.textContent
//         ) {
//           rowUpdateNow = sliderValue10.textContent;
//         }
//       }
//     }
//   }
// }
