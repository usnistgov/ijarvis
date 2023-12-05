var myMinMaxObj = {
  "OPT-bandgap": [8, "opgtbox", "opltbox"],
  "MBJ-bandgap": [9, "mbjgtbox", "mbjltbox"],
  "HSE-bandgap": [10, "hsegtbox", "hseltbox"],
  "Bulk-mod": [11, "bvgtbx", "bvltbox"],
  "Shear-mod": [12, "gvgtbx", "gvltbox"],
  "Formation-energy": [14, "fgtbox", "fltbox"],
  "Exfoliation-energy": [16, "exfgtbox", "exfltbox"],
  "Spg. numb": [3, "spggtbox", "spgltbox"],
  Density: [5, "densitygtbox", "densityltbox"],
  "SOC-Spillage": [15, "spillgtbox", "spillltbox"],
  SLME: [17, "slmegtbox", "slmeltbox"],
  MagMom: [18, "maggtbox", "magltbox"],
  nats: [19, "natsgtbox", "natsltbox"],
};

//load myMinMaxObj on load
window.onload = () => {
  //make_header();
};

//console.log("box_inpt", box_inpt);
//console.log("jid1", document.getElementById("jidbox").value, results[0][0][0]);
function make_header() {
  var table = document.getElementById("table-sort");
  document.getElementById("table-sort").innerHTML = "";
  var header = table.createTHead();
  var row = header.insertRow(0);
  row.style.backgroundColor = "#00CED1";
  var cell = row.insertCell(0);
  cell.innerHTML = "<b>JARVIS-ID</b>";
  var cell = row.insertCell(1);
  cell.innerHTML = "<b>Formula</b>";
  var cell = row.insertCell(2);
  cell.innerHTML = "<b>Spg. symb</b>";
  var cell = row.insertCell(3);
  cell.innerHTML = "<b>Spg. numb</b>";
  var cell = row.insertCell(4);
  cell.innerHTML = "<b>Cryst.-sys</b>";

  var cell = row.insertCell(5);
  cell.innerHTML = "<b>Density</b>";
  var cell = row.insertCell(6);
  //cell.innerHTML = "<b>MPID</b>";
  //var cell = row.insertCell(4)
  cell.innerHTML = "<b>Func.</b>";
  var cell = row.insertCell(7);
  cell.innerHTML = "<b>Calc.  type</b>";
  var cell = row.insertCell(8);
  cell.innerHTML = "<b>OPT-bandgap</b>";
  var cell = row.insertCell(9);
  cell.innerHTML = "<b>MBJ-bandgap</b>";
  var cell = row.insertCell(10);
  cell.innerHTML = "<b>HSE-bandgap</b>";
  var cell = row.insertCell(11);
  cell.innerHTML = "<b>B<sub>v</sub> (GPa)</b>";
  var cell = row.insertCell(12);
  cell.innerHTML = "<b>G<sub>v</sub> (GPa)</b>";
  var cell = row.insertCell(13);
  cell.innerHTML = "<b>Poisson ratio</b>";
  var cell = row.insertCell(14);
  cell.innerHTML = "<b>Formation energy (eV/atom)</b>";

  var cell = row.insertCell(15);
  cell.innerHTML = "<b>SOC-Spillage</b>";

  var cell = row.insertCell(16);
  cell.innerHTML = "<b>Exfoliation energy (meV/atom)</b>";

  var cell = row.insertCell(17);
  cell.innerHTML = "<b>SLME (%)</b>";

  var cell = row.insertCell(18);
  cell.innerHTML = "<b>Mag. mom</b>";
  var cell = row.insertCell(19);
  cell.innerHTML = "<b>nAtoms</b>";

  var cell = row.insertCell(20);
  cell.innerHTML = "<b>Other links</b>";
}

function sortFunction(a, b) {
  window.scrollTo(0, document.body.scrollHeight);
  if (a[14] === b[14]) {
    return 0;
  } else {
    return a[14] > b[14] ? -1 : 1;
  }
}
function jurl2jid(url) {
  var jid = url.split("target='_blank' >")[1].split("</a>")[0];
  return jid;
}
function advsearch() {
  //console.log("box_inpt", box_inpt);
  //var input_txt = input.value; //box_inpt;
  tmp = results;

  if (
    typeof document.getElementById("mytext") != "undefined" &&
    document.getElementById("mytext").value != ""
  ) {
    var inp_txt = possibl_els(document.getElementById("mytext").value);

    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("inpp", inp_txt);
    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("comp1", inp_els);
    //console.log("comp2", f);
    var tmp_el_arr = [];
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");

    var table = document.getElementById("table-sort");
    for (i = 0; i < search.length; i++) {
      if (search[i] == f) {
        now_results = results[i];
        tmp_el_arr.push(now_results);
      }
    }
    tmp = tmp_el_arr;

    var container = document
      .getElementById("container")
      .getElementsByTagName("div");
    //desect_others(tmp_el_arr, f, container);
  }

  for (var key in myMinMaxObj) {
    // check if the property/key is defined in the object itself, not in parent
    if (myMinMaxObj.hasOwnProperty(key)) {
      var index = myMinMaxObj[key];
      //console.log("index",index);
      var element1 = document.getElementById("compobox").value;
      //console.log("is null?", (index[1],document.getElementById(index[1]).value));
      var element2 = document.getElementById("jidbox").value;
      //console.log("is null?", document.getElementById(index[1]));
      if (element1 != "" && element2 != "") {
        var maxval = element1;
        var minval = element2;

        var indexval = index[0];
        //console.log("minmax", indexval, minval, maxval);
        //console.log("tmp_arr", tmp_arr);

        var tmp = make_adv_table_for_index(indexval, maxval, minval, tmp);
      }
    }
  }

  //tmp = results;
  var inp_jid = document.getElementById("jidbox").value;
  if (inp_jid != "") {
    //console.log("jid2", inp_jid);
    for (i = 0; i < search.length; i++) {
      for (j = 0; j < results[i].length; j++) {
        if (results[i][j][0] != "undefined" && results[i][j][0] != "--") {
          //console.log("jide",results[i][j][0] );
          tmp_jid = jurl2jid(results[i][j][0]);
          //console.log("jide", tmp_jid);
          if (tmp_jid === inp_jid) {
            //console.log("dfghj", results[i][j], inp_jid);
            //console.log("dfghj2", results[i][j][0]);
            tmp = [[results[i][j]]];
          }
        }
      }
    }
  }

  var inp_crys = document.getElementById("crys").value;
  if (inp_crys != "") {
    var crys_array = [];
    //console.log("jid2", inp_jid);
    for (i = 0; i < search.length; i++) {
      for (j = 0; j < results[i].length; j++) {
        if (results[i][j][4] != "undefined" && results[i][j][4] != "--") {
          //console.log("jide",results[i][j][0] );

          //console.log("jide", tmp_jid);
          if (inp_crys === results[i][j][4]) {
            //console.log("dfghj", results[i][j], inp_jid);
            //console.log("dfghj2", results[i][j][0]);
            //tmp = [[results[i][j]]];
            crys_array.push([results[i][j]]);
          }
        }
      }
    }
    tmp = crys_array;
  }

  var inp_els = document.getElementById("compobox").value;
  if (inp_els != "") {
    var f = inp_els.split("-").sort();
    var f = f.join("-");
    //console.log("comp1", inp_els);
    //console.log("comp2", f);
    var tmp_el_arr = [];
    //var container = document
    // .getElementById("container")
    // .getElementsByTagName("div");

    var table = document.getElementById("table-sort");
    for (i = 0; i < search.length; i++) {
      if (search[i] == f) {
        now_results = results[i];
        tmp_el_arr.push(now_results);
      }
    }
    tmp = tmp_el_arr;
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");
    //desect_others(tmp_el_arr, f, container);
    // window.scrollTo(0, document.body.scrollHeight);
  }

  //console.log("index", index);
  //make_header();
  document.getElementById("pText").innerHTML =
    "Results Found: " + tmp[0].length;
  make_filtered_tables(tmp);
  //console.log("tmp", tmp, tmp.length);
  //make_table();
}

function isItNumber(str) {
  return /^\-?[0-9]+(e[0-9]+)?(\.[0-9]+)?$/.test(str);
}

function make_adv_table_for_index(filter_index, minn, maxx, res) {
  var array = [];
  //console.log("filter arr1", results[0][0][5]);
  for (i = 0; i < res.length; i++) {
    for (j = 0; j < res[i].length; j++) {
      var tmp = res[i][j][filter_index];

      if (
        isItNumber(tmp) &&
        parseFloat(tmp) >= minn &&
        parseFloat(tmp) <= maxx
      ) {
        //console.log("success");
        //console.log("tmppp", tmp, minn, maxx, res[i][j][0]);
        array.push(res[i][j]);
        //console.log("filter arr", arr);
      }
    }
    //console.log("MinMax", min, max);
  }
  //console.log("arr success", arr);

  return [array];
}

function make_filtered_tables(data) {
  window.scrollTo(0, document.body.scrollHeight);
  var table = document.getElementById("table-sort");
  for (i = 0; i < data.length; i++) {
    var now_results = data[i];
    for (j = 0; j < now_results.length; j++) {
      var row = table.insertRow(-1);
      var tmp_now = now_results[j];

      for (k = 0; k < tmp_now.length - 2; k++) {
        var cell = row.insertCell(k);
        cell.innerHTML = tmp_now[k];
      }
    }
  }
}

function add(ev) {
  var elt_name = ev.target.id + "-";
  var formulabox = document.getElementById("mytext");
  var oldformula = formulabox.value;
  //console.log("formulabox.value", document.getElementById("mytext").value);
  if (oldformula.indexOf(elt_name) != -1) {
    formulabox.value = oldformula.replace(elt_name, "");
    // document.getElementById(ev.target.id).style.backgroundColor = "black";
  } else {
    formulabox.value = oldformula + elt_name; //removed old name, this will refresh search per click
    // document.getElementById(ev.target.id).style.backgroundColor = "#FFA500"; //on click already shows effect
    //console.log("Elem " + document.getElementById(ev.target.id).textContent); //test on click
  }
  box_inpt = formulabox.value;
  return box_inpt;
  //console.log("box_inpt", box_inpt);
}

function desect_others(now_results, f, container) {
  for (ii = 0; ii < search.length; ii++) {
    var array = search[ii];
    //if (f in search[ii]){
    // cons ole.log("success",search[ii]);
    //}

    //delete tmp[0];
    var container = container;
    var tmp = f.split("-").sort();
    //console.log("tmp=", tmp);
    var tmp1 = tmp.join("-");
    var dumb = tmp1.concat("-");
    //console.log("dumb", dumb);
    //onsole.log("tmp1", tmp1);
    if (array.includes(dumb)) {
      //console.log(dumb, array);

      var array1 = array.concat("-").split("-");
      //console.log(array1);

      //var child_tmp = container[ids].id;
      //console.log("child length", child_tmp.length);
      for (jids = 0; jids < container.length; jids++) {
        if (array1.includes(container[jids].id)) {
          //console.log('jid',array1,tmp,child_tmp[jids]);
          container[jids].style.backgroundColor = "#FFA500";
        }
      }
    }

    window.scrollTo(0, document.body.scrollHeight);
  }
}
var myObj = {
  "JARVIS-ID": 0,
  Formula: 1,
  "Space-group": [2, "spgbox"],
  "Calculation type": [
    3,
    "3D-bulk",
    "2D-bulk",
    "1D-bulk",
    "0D-bulk",
    "2D-1L",
    "2D-2L",
    "2D-3L",
  ],
  "OPT-bandgap": [4, "opgtbox", "opltbox"],
  "MBJ-bandgap": [5, "mbjgtbox", "mbjltbox"],
  "HSE-bandgap": [6, "hsegtbox", "hseltbox"],
  "Kv (GPa)": [7, "bvgtbx", "bvltbox"],
  "Gv (GPa)": [8, "gvgtbx", "gvltbox"],
  "Formation energy (eV/atom)": [9, "fgtbox", "fltbox"],
  "Exfoliation energy (meV/atom)": [10, "exfgtbox", "exfltbox"],
  "SOC-Spillage": [11, "spillgtbox", "spillltbox"],
  "Other links": 12,
};

//console.log("stuff", myObj.Formula);

/*
for (var key in myObj) {
  // check if the property/key is defined in the object itself, not in parent
  if (myObj.hasOwnProperty(key)) {
    console.log("lelelele", key, myObj[key]);
  }
}
*/

//var filterIds = ["mbjgtbox", "mbjltbox"];

function getFilterId(specificId) {
  var filterId = document.getElementById(specificId);
  return filterId;
}
//console.log("id values", filterIds.forEach(getFilterId));
//console.log("filter value", getFilterId("optltbox"));

function make_table(f) {
  var container = document
    .getElementById("container")
    .getElementsByTagName("div");
  for (ids = 0; ids < container.length; ids++) {
    container[ids].style.backgroundColor = "#F4F4F4";
  }
  var table = document.getElementById("table-sort");
  for (i = 0; i < search.length; i++) {
    if (search[i] == f) {
      console.log("success");

      now_results = results[i];
      now_results.sort(sortFunction);
      for (j = 0; j < now_results.length; j++) {
        var row = table.insertRow(-1);
        var tmp_now = now_results[j];

        for (k = 0; k < tmp_now.length - 2; k++) {
          var cell = row.insertCell(k);
          cell.innerHTML = tmp_now[k];
        }
      }
    }
  }

  document.getElementById("pText").innerHTML =
    "Results Found: " + now_results.length;
  desect_others(now_results, f, container);
  window.scrollTo(0, document.body.scrollHeight);
}

function sortFunction(a, b) {
  window.scrollTo(0, document.body.scrollHeight);
  if (a[14] === b[14]) {
    return 0;
  } else {
    return a[14] > b[14] ? -1 : 1;
    //window.scrollTo(0,document.body.scrollHeight);
  }
}

//make table based on the input value == row of table data

let tableUpdate = document.getElementById("table-sort");
let rowUpdate = tableUpdate.rows; //number of rows initially

//OPT bandgap
function optSlider() {
  let sliderOpt = document.getElementById("opgtbox");
  let sliderValue = document.getElementById("sliderValues");

  sliderOpt.addEventListener("input", function () {
    sliderValue.textContent = sliderOpt.value;
    rowUpdate = sliderValue.textContent;
    console.log("OPt slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//MBJ bandgap
function mbgSlider() {
  let sliderOpt1 = document.getElementById("mbjgtbox");
  let sliderValue1 = document.getElementById("sliderValues1");
  let rowMbg;
  sliderOpt1.addEventListener("input", function () {
    sliderValue1.textContent = sliderOpt1.value;
    rowUpdate = sliderValue1.textContent;

    rowMbg = sliderValue1.textContent;

    console.log("MBG slider row update is " + rowUpdate);
    return rowMbg;
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  applySliderFilterTable(rowUpdate);
}

//HSE-bandgap
function hseSlider() {
  let sliderOpt2 = document.getElementById("hsegtbox");
  let sliderValue2 = document.getElementById("sliderValues2");

  sliderOpt2.addEventListener("input", function () {
    // slider value to text
    sliderValue2.textContent = sliderOpt2.value;
    rowUpdate = sliderValue2.textContent;
    console.log("HSE slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  //makeTable(rowUpdate);
}
//add Kv
//GV
function gvSlider() {
  let sliderOpt4 = document.getElementById("gvgtbx");
  let sliderValue4 = document.getElementById("sliderValues4");

  sliderOpt4.addEventListener("input", function () {
    // slider value to text
    sliderValue4.textContent = sliderOpt4.value;
    rowUpdate = sliderValue4.textContent;
    console.log("GV slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  applySliderFilterTable(rowUpdate);
}

//FORMATION
function formationSlider() {
  let sliderOpt5 = document.getElementById("fgtbox");
  let sliderValue5 = document.getElementById("sliderValues5");

  sliderOpt5.addEventListener("input", function () {
    // slider value to text
    sliderValue5.textContent = sliderOpt5.value;
    rowUpdate = sliderValue5.textContent;
    console.log("HSE slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//Exfoliation
function exfoliationSlider() {
  let sliderOpt6 = document.getElementById("exfgtbox");
  let sliderValue6 = document.getElementById("sliderValues6");

  sliderOpt6.addEventListener("input", function () {
    // slider value to text
    sliderValue6.textContent = sliderOpt6.value;
    rowUpdate = sliderValue6.textContent;
    console.log("Exfoliation slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//SPILLAGE
function spillageSlider() {
  let sliderOpt7 = document.getElementById("spillgtbox");
  let sliderValue7 = document.getElementById("sliderValues7");

  sliderOpt7.addEventListener("input", function () {
    // slider value to text
    sliderValue7.textContent = sliderOpt7.value;
    rowUpdate = sliderValue7.textContent;
    console.log("SPILLAGE slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//SLME
function slmeSlider() {
  let sliderOpt8 = document.getElementById("slmegtbox");
  let sliderValue8 = document.getElementById("sliderValues8");

  sliderOpt8.addEventListener("input", function () {
    // slider value to text
    sliderValue8.textContent = sliderOpt8.value;
    rowUpdate = sliderValue8.textContent;
    console.log("SLME slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  applySliderFilterTable(rowUpdate);
}

//MAGMOM
function magMom() {
  let sliderOpt9 = document.getElementById("maggtbox");
  let sliderValue9 = document.getElementById("sliderValues9");

  sliderOpt9.addEventListener("input", function () {
    // slider value to text
    sliderValue9.textContent = sliderOpt9.value;
    rowUpdate = sliderValue9.textContent;
    console.log("MAGMOM slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  applySliderFilterTable(rowUpdate);
}

//DENSITY
function densitySlider() {
  let sliderOpt10 = document.getElementById("densitygtbox");
  let sliderValue10 = document.getElementById("sliderValues10");

  sliderOpt10.addEventListener("input", function () {
    // slider value to text
    sliderValue10.textContent = sliderOpt10.value;
    rowUpdate = sliderValue10.textContent;
    console.log("DENSITY slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//SPG
function spgSlider() {
  let sliderOpt11 = document.getElementById("spggtbox");
  let sliderValue11 = document.getElementById("sliderValues11");

  sliderOpt11.addEventListener("input", function () {
    // slider value to text
    sliderValue11.textContent = sliderOpt11.value;
    rowUpdate = sliderValue11.textContent;
    console.log("SPG slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  // applySliderFilterTable(rowUpdate);
}

//NUMBER OF ATOMS
function numberOfAtoms() {
  //nAtoms
  let sliderOpt12 = document.getElementById("natsgtbox");
  let sliderValue12 = document.getElementById("sliderValues12");

  sliderOpt12.addEventListener("input", function () {
    // slider value to text
    sliderValue12.textContent = sliderOpt12.value;
    rowUpdate = sliderValue12.textContent;
    console.log("SPG slider row update is " + rowUpdate);
  });

  //call make table function with row update makeTable(rowUpdate)  rows == rowUpdate.length;
  applySliderFilterTable(rowUpdate);
}

//NEW TABLE WITH ROWUPDATES
function applySliderFilterTable(rowUpdate) {
  let mbgValue = mbgSlider();
  for (j = 0; j < rowUpdate.length; j++) {
    if (j[9] <= rowMbg) {
    }
    var row = table.insertRow(-1);
    var tmp_now = rowUpdate[j];

    for (k = 0; k < tmp_now.length - 2; k++) {
      var cell = row.insertCell(k);
      cell.innerHTML = tmp_now[k];
    }
  }
}

//ADD EVENT LISTENERS TO INPUTS
optSlider();
mbgSlider();
hseSlider();
densitySlider();
