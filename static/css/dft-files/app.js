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
  tableStyle.classList.remove("myTableStyle");
  tableStyle.classList.add("tableSection");
  tableStyle.style.display = "flex";
  newTable.style.display = "flex";
  pTextDisplayEffect.classList.add("output-results-texts-effect");
});

//Re-arrange Tables
//Store Table data
const th = document.getElementsByClassName("theader");

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
let sliderOpt2Min = document.getElementById("hsegtbox_l");
let sliderOpt2 = document.getElementById("hsegtbox");
let sliderValue2Min = document.getElementById("sliderValues2Min");
let sliderValue2 = document.getElementById("sliderValues2");
// slider value to text
sliderValue2Min.textContent = sliderOpt2Min.value;
sliderValue2.textContent = sliderOpt2.value;
//activate slider values
sliderOpt2.oninput = function () {
  sliderValue2.textContent = sliderOpt2.value;
};
//activate min
sliderOpt2Min.oninput = function () {
  sliderValue2Min.textContent = sliderOpt2Min.value;
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
  sliderValue3.textContent = sliderOpt3.value;
};
//min slider values
sliderOpt3Min.oninput = function () {
  sliderValue3Min.textContent = sliderOpt3Min.value;
};

//GV
let sliderOpt4 = document.getElementById("gvgtbx");
let sliderOpt4Min = document.getElementById("gvgtbx_l");
let sliderValue4 = document.getElementById("sliderValues4");
let sliderValue4Min = document.getElementById("sliderValues4Min");
// slider value to text
sliderValue4Min.textContent = sliderOpt4Min.value;
sliderValue4.textContent = sliderOpt4.value;
//activate max slider values
sliderOpt4.oninput = function () {
  sliderValue4.textContent = sliderOpt4.value;
};

//min gv activation
sliderOpt4Min.oninput = function () {
  sliderValue4Min.textContent = sliderOpt4Min.value;
};

//FORMATION
let sliderOpt5Min = document.getElementById("fgtbox_l");
let sliderOpt5 = document.getElementById("fgtbox");
let sliderValue5Min = document.getElementById("sliderValues5Min");
let sliderValue5 = document.getElementById("sliderValues5");
// slider value to text
sliderValue5Min.textContent = sliderOpt5Min.value;
sliderValue5.textContent = sliderOpt5.value;
//activate slider values
sliderOpt5.oninput = function () {
  sliderValue5.textContent = sliderOpt5.value;
};
//min activation
sliderOpt5Min.oninput = function () {
  sliderValue5Min.textContent = sliderOpt5Min.value;
};

//Exfoliation
let sliderOpt6 = document.getElementById("exfgtbox");
let sliderOpt6Min = document.getElementById("exfgtbox_l");
let sliderValue6 = document.getElementById("sliderValues6");
let sliderValue6Min = document.getElementById("sliderValues6Min");
// slider value to text
sliderValue6Min.textContent = sliderOpt6Min.value;
sliderValue6.textContent = sliderOpt6.value;
//activate slider values
sliderOpt6.oninput = function () {
  sliderValue6.textContent = sliderOpt6.value;
};

//min activate
sliderOpt6Min.oninput = function () {
  sliderValue6Min.textContent = sliderOpt6Min.value;
};

//SPILLAGE
let sliderOpt7Min = document.getElementById("spillgtbox_l");
let sliderOpt7 = document.getElementById("spillgtbox");
let sliderValue7Min = document.getElementById("sliderValues7Min");
let sliderValue7 = document.getElementById("sliderValues7");
// slider value to text
sliderValue7Min.textContent = sliderOpt7Min.value;
sliderValue7.textContent = sliderOpt7.value;
//activate slider values
sliderOpt7.oninput = function () {
  sliderValue7.textContent = sliderOpt7.value;
};
//activate min slider values
sliderOpt7Min.oninput = function () {
  sliderValue7Min.textContent = sliderOpt7Min.value;
};

//SLME
let sliderOpt8Min = document.getElementById("slmegtbox_l");
let sliderOpt8 = document.getElementById("slmegtbox");
let sliderValue8Min = document.getElementById("sliderValues8Min");
let sliderValue8 = document.getElementById("sliderValues8");
// slider value to text
sliderValue8Min.textContent = sliderOpt8Min.value;
sliderValue8.textContent = sliderOpt8.value;
//activate slider values
sliderOpt8.oninput = function () {
  sliderValue8.textContent = sliderOpt8.value;
};
//activate min slider values
sliderOpt8Min.oninput = function () {
  sliderValue8Min.textContent = sliderOpt8Min.value;
};

//MAGMOM
let sliderOpt9Min = document.getElementById("maggtbox_l");
let sliderValue9Min = document.getElementById("sliderValues9Min");
let sliderOpt9 = document.getElementById("maggtbox");
let sliderValue9 = document.getElementById("sliderValues9");
// slider value to text
sliderValue9Min.textContent = sliderOpt9Min.value;
sliderValue9.textContent = sliderOpt9.value;
//activate min slider values
sliderOpt9Min.oninput = function () {
  sliderValue9Min.textContent = sliderOpt9Min.value;
};
//activate slider values
sliderOpt9.oninput = function () {
  sliderValue9.textContent = sliderOpt9.value;
};

//DENSITY
let sliderOpt10Min = document.getElementById("densitygtbox_l");
let sliderValue10Min = document.getElementById("sliderValues10Min");
let sliderOpt10 = document.getElementById("densitygtbox");
let sliderValue10 = document.getElementById("sliderValues10");

// slider value to text
sliderValue10Min.textContent = sliderOpt10Min.value;
sliderValue10.textContent = sliderOpt10.value;
//activate slider values
sliderOpt10Min.oninput = function () {
  sliderValue10Min.textContent = sliderOpt10Min.value;
};
//activate min slider
sliderOpt10.oninput = function () {
  sliderValue10.textContent = sliderOpt10.value;
};

//SPG
let sliderOpt11Min = document.getElementById("spggtbox_l");
let sliderValue11Min = document.getElementById("sliderValues11Min");
let sliderOpt11 = document.getElementById("spggtbox");
let sliderValue11 = document.getElementById("sliderValues11");
// slider value to text
sliderValue11Min.textContent = sliderOpt11Min.value;
sliderValue11.textContent = sliderOpt11.value;
//activate min slider values
sliderOpt11Min.oninput = function () {
  sliderValue11Min.textContent = sliderOpt11Min.value;
};
//activate slider values
sliderOpt11.oninput = function () {
  sliderValue11.textContent = sliderOpt11.value;
};

//nAtoms
let sliderOpt12Min = document.getElementById("natsgtbox_l");
let sliderValue12Min = document.getElementById("sliderValues12Min");
let sliderOpt12 = document.getElementById("natsgtbox");
let sliderValue12 = document.getElementById("sliderValues12");
// slider value to text
sliderValue12Min.textContent = sliderOpt12Min.value;
sliderValue12.textContent = sliderOpt12.value;

//activate slider values
sliderOpt12Min.oninput = function () {
  sliderValue12Min.textContent = sliderOpt12Min.value;
};

//activate slider values
sliderOpt12.oninput = function () {
  sliderValue12.textContent = sliderOpt12.value;
};

//Navigation Menu
const press_menu_button = document.getElementById("press_button");
const display_menu = document.getElementById("menu_list");
const move_intro_section = document.getElementById("intro_section");

//Animation Function on Pressing menu
press_menu_button.addEventListener("click", function pressButton() {
  if (display_menu.style.display != "flex") {
    display_menu.style.display = "flex";
    move_intro_section.classList.add("jumbo_section_move_down");
    press_menu_button.src = "/images/menu-cancel.svg"; // src = https://img.icons8.com/ios-filled/344/ffffff/cancel.png
  } else {
    display_menu.style.display = "none";
    move_intro_section.classList.remove("jumbo_section_move_down");
    press_menu_button.src = "/images/menu-icon.svg";
  }
});
