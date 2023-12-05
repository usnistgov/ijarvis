//column in results,maxbox,minbox,maxval,minval

var myMinMaxObj = {
  "OPT-bandgap": [8, "opgtbox", "opgtbox_l",15,0],
  "MBJ-bandgap": [9, "mbjgtbox", "mbjgtbox_l",15,0],
  "HSE-bandgap": [10, "hsegtbox", "hsegtbox_l",15,0],
  "Bulk-mod": [11, "kvgtbx", "kvgtbx_l",500,-5],
  "Shear-mod": [12, "gvgtbx", "gvgtbx_l",500,-5],
  "Formation-energy": [14, "fgtbox", "fgtbox_l",5,-5],
  "Exfoliation-energy": [16, "exfgtbox", "exfgtbox_l",1000,0],
  "Spg. numb": [3, "spggtbox", "spggtbox_l",230,1],
  "Density": [5, "densitygtbox", "densitygtbox_l",25,0],
  "SOC-Spillage": [15, "spillgtbox", "spillgtbox_l",5,0],
  "SLME": [17, "slmegtbox", "slmegtbox_l",34,0],
  "MagMom": [18, "maggtbox", "maggtbox_l",500,0],
  "nats": [19, "natsgtbox", "natsgtbox_l",1000,1],
};

var myMinMaxObj = {
};
//load myMinMaxObj on load
window.onload = () => {
  //make_header();
};

//console.log("box_inpt", box_inpt);
//console.log("jid1", document.getElementById("jidbox").value, results[0][0][0]);


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
  var tmp = results;
  if (
    typeof document.getElementById("mytext") != "undefined" &&
    document.getElementById("mytext").value != ""
  ) {
    var inp_txt = possibl_els(document.getElementById("mytext").value);

    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("inpp111", inp_txt);
    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("comp1", inp_els);
    //console.log("comp2", f);
    var tmp_el_arr = [];
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");

    //var table = document.getElementById("table-sort");
    var link1='<a href="https://www.ctcms.nist.gov/~knc6/DOWNLOADS/" target="_blank">'
    for (i = 0; i < search.length+1; i++) {
      if (search[i] == f) {
        now_results = results[i];
	//console.log('tmp222',i,search[i],f,results[i]);
        //console.log('tmp222x',results[i][0][3]);
	for (j = 0; j < now_results.length; j++){
		//console.log('now_results',now_results);
		//console.log('now_results3',now_results);
		now_results[j][3]='<a href="https://www.ctcms.nist.gov/~knc6/DOWNLOADS/'+now_results[j][3]+'" target="_blank">'+now_results[j][3]+'</a>'; //link1.concat(now_results[3]);
		//console.log('now_results[j][3]',now_results[j][3]);
	}
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
      //console.log("index", document.getElementById(index[1]).value, document.getElementById(index[2]).value);
      var element1 = document.getElementById(index[1]).value
      var element2 = document.getElementById(index[2]).value
	    //document.getElementById("compobox").value;
      //console.log("is null?", (index[1],document.getElementById(index[1]).value));
      //console.log("is null?", document.getElementById(index[1]));
      if (element1 != "" && element2 != "" && element1!=index[3] &&element2!=index[4]) {
        var maxval = element1;
        var minval = element2;

        var indexval = index[0];
        //console.log("minmax", indexval, minval, maxval);
        //console.log("tmp_arr", tmp_arr);
        //console.log('tmo1',tmp);
        var tmp = make_adv_table_for_index(indexval, minval,maxval, tmp);
        //console.log('tmo2',tmp);
      }
    }
  }

  //tmp = results;
  var inp_jid = document.getElementById("jidbox").value;
  if (inp_jid != "") {
    //console.log("jid2", inp_jid);
    for (i = 0; i < search.length+1; i++) {
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

    //var table = document.getElementById("table-sort");
    for (i = 0; i < search.length; i++) {
      if (search[i] == f) {
        now_results = results[i];
        tmp_el_arr.push(now_results);
      }
    }
    tmp = tmp_el_arr;
    console.log('tmp',tmp);
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");
    //desect_others(tmp_el_arr, f, container);
    // window.scrollTo(0, document.body.scrollHeight);
  }
  

  //console.log("tmp111", tmp);
  //make_header();
  //console.log('Results found',tmp[0].length);
  document.getElementById("pText").innerHTML =
  "Results Found: " + tmp[0].length;
  make_filtered_tables(tmp);
  //console.log("tmp", tmp, tmp.length);
  //make_table();
 }

function advsearch2() {
  //console.log("box_inpt", box_inpt);
  //var input_txt = input.value; //box_inpt;
  var tmp = results;
  if (
    typeof document.getElementById("mytext") != "undefined" &&
    document.getElementById("mytext").value != ""
  ) {
    var inp_txt = possibl_els(document.getElementById("mytext").value);

    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("inpp111", inp_txt);
    var f = inp_txt.split("-").sort();
    var f = f.join("-");
    //console.log("comp1", inp_els);
    //console.log("comp2", f);
    var tmp_el_arr = [];
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");

    var table = document.getElementById("table-sort");
    var rowCount = table.rows.length;
    var tableHeaderRowCount = 1;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
       table.deleteRow(tableHeaderRowCount);
       }
    for (i = 0; i < search.length+1; i++) {
      if (search[i] == f) {
        now_results = results[i];
        //console.log('tmp222',i,search[i],f,results[i]);
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
      //console.log("index", document.getElementById(index[1]).value, document.getElementById(index[2]).value);
      var element1 = document.getElementById(index[1]).value
      var element2 = document.getElementById(index[2]).value
	    //document.getElementById("compobox").value;
      //console.log("is null?", (index[1],document.getElementById(index[1]).value));
      //console.log("is null?", document.getElementById(index[1]));
      if (element1 != "" && element2 != "" && element1!=index[3] &&element2!=index[4]) {
        var maxval = element1;
        var minval = element2;

        var indexval = index[0];
        //console.log("minmax", indexval, minval, maxval);
        //console.log("tmp_arr", tmp_arr);
        //console.log('tmo1',tmp);
        var tmp = make_adv_table_for_index(indexval, minval,maxval, tmp);
        //console.log('tmo2',tmp);
      }
    }
  }

  //tmp = results;
  var inp_jid = document.getElementById("jidbox").value;
  if (inp_jid != "") {
    //console.log("jid2", inp_jid);
    for (i = 0; i < search.length+1; i++) {
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

    //var table = document.getElementById("table-sort2");
    for (i = 0; i < search.length; i++) {
      if (search[i] == f) {
        now_results = results[i];
        tmp_el_arr.push(now_results);
      }
    }
    tmp = tmp_el_arr;
    console.log('tmp',tmp);
    var container = document
      .getElementById("container")
      .getElementsByTagName("div");
    //desect_others(tmp_el_arr, f, container);
    // window.scrollTo(0, document.body.scrollHeight);
  }
  

  //console.log("tmp111", tmp);
  //make_header();
  //console.log('Results found',tmp[0].length);
  document.getElementById("pText").innerHTML =
  "Results Found: " + tmp[0].length;
  make_filtered_tables2(tmp);
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
    var rowCount = table.rows.length;
    var tableHeaderRowCount = 1;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
       table.deleteRow(tableHeaderRowCount);
       }



  for (i = 0; i < data.length; i++) {
    var now_results = data[i];
    for (j = 0; j < now_results.length; j++) {
      var row = table.insertRow(-1);
      var tmp_now = now_results[j];

      for (k = 0; k < tmp_now.length ; k++) {
        var cell = row.insertCell(k);
        cell.innerHTML = tmp_now[k];
      }
    }
  }
}

function make_filtered_tables2(data) {
  window.scrollTo(0, document.body.scrollHeight);
  var table = document.getElementById("table-sort");
    var rowCount = table.rows.length;
    var tableHeaderRowCount = 1;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
       table.deleteRow(tableHeaderRowCount);
       }
  for (i = 0; i < data.length; i++) {
    var now_results = data[i];
    for (j = 0; j < now_results.length; j++) {
      var row = table.insertRow(-1);
      var tmp_now = now_results[j];

      for (k = 0; k < tmp_now.length ; k++) {
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
  if (oldformula.indexOf(elt_name) != -1) {
    formulabox.value = oldformula.replace(elt_name, "");
    document.getElementById(ev.target.id).style.backgroundColor = "black";
  } else {
    formulabox.value = oldformula + elt_name;
    document.getElementById(ev.target.id).style.backgroundColor = "#C0C0C0";
  }
  box_inpt = formulabox.value;
  //console.log("box_inpt111", box_inpt);
  return box_inpt;
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
    var rowCount = table.rows.length;
    var tableHeaderRowCount = 1;
    for (var i = tableHeaderRowCount; i < rowCount; i++) {
       table.deleteRow(tableHeaderRowCount);
       }
  for (i = 0; i < search.length; i++) {
    if (search[i] == f) {
      console.log("success");

      now_results = results[i];
      now_results.sort(sortFunction);
      for (j = 0; j < now_results.length; j++) {
        var row = table.insertRow(-1);
        var tmp_now = now_results[j];

        for (k = 0; k < tmp_now.length ; k++) {
          var cell = row.insertCell(k);
          cell.innerHTML = tmp_now[k];
        }
      }
    }
  }

  /////document.getElementById("pText").innerHTML =
  ////  "Results Found: " + now_results.length;
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
  let sliderOptMax = document.getElementById("opgtbox");
  let sliderOptMin = document.getElementById("opgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues");
  let sliderValueMin1 = document.getElementById("sliderValuesMin");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("OPT slider row update is " ,document.getElementById("opgtbox").value, document.getElementById("opgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
    //console.log("OPT slider row update is " ,document.getElementById("opgtbox").value, document.getElementById("opgtbox_l").value);
  });
}

//MBJ bandgap
function mbjSlider() {
  let sliderOptMax = document.getElementById("mbjgtbox");
  let sliderOptMin = document.getElementById("mbjgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues1");
  let sliderValueMin1 = document.getElementById("sliderValuesMin1");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}





//HSE-bandgap
function hseSlider() {
  let sliderOptMax = document.getElementById("hsegtbox");
  let sliderOptMin = document.getElementById("hsegtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues2");
  let sliderValueMin1 = document.getElementById("sliderValuesMin2");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}

//Kv
function kvSlider() {
  let sliderOptMax = document.getElementById("kvgtbx");
  let sliderOptMin = document.getElementById("kvgtbx_l");
  let sliderValueMax1 = document.getElementById("sliderValues3");
  let sliderValueMin1 = document.getElementById("sliderValuesMin3");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}



//Gv
function gvSlider() {
  let sliderOptMax = document.getElementById("gvgtbx");
  let sliderOptMin = document.getElementById("gvgtbx_l");
  let sliderValueMax1 = document.getElementById("sliderValues4");
  let sliderValueMin1 = document.getElementById("sliderValuesMin4");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}


//formation
function formationSlider() {
  let sliderOptMax = document.getElementById("fgtbox");
  let sliderOptMin = document.getElementById("fgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues5");
  let sliderValueMin1 = document.getElementById("sliderValuesMin5");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}


//exfo
function exfoliationSlider() {
  let sliderOptMax = document.getElementById("exfgtbox");
  let sliderOptMin = document.getElementById("exfgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues6");
  let sliderValueMin1 = document.getElementById("sliderValuesMin6");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}




//SPILLAGE
function spillageSlider() {
  let sliderOptMax = document.getElementById("spillgtbox");
  let sliderOptMin = document.getElementById("spillgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues7");
  let sliderValueMin1 = document.getElementById("sliderValuesMin7");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}









//SLME
function slmeSlider() {
  let sliderOptMax = document.getElementById("slmegtbox");
  let sliderOptMin = document.getElementById("slmegtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues8");
  let sliderValueMin1 = document.getElementById("sliderValuesMin8");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}







//MAGMOM
function magSlider() {
  let sliderOptMax = document.getElementById("maggtbox");
  let sliderOptMin = document.getElementById("maggtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues9");
  let sliderValueMin1 = document.getElementById("sliderValuesMin9");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}







//DENSITY
function densitySlider() {
  let sliderOptMax = document.getElementById("densitygtbox");
  let sliderOptMin = document.getElementById("densitygtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues10");
  let sliderValueMin1 = document.getElementById("sliderValuesMin10");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}







//SPG

function spgSlider() {
  let sliderOptMax = document.getElementById("spggtbox");
  let sliderOptMin = document.getElementById("spggtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues11");
  let sliderValueMin1 = document.getElementById("sliderValuesMin11");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}





//NUMBER OF ATOMS
function natsSlider() {
  let sliderOptMax = document.getElementById("natsgtbox");
  let sliderOptMin = document.getElementById("natsgtbox_l");
  let sliderValueMax1 = document.getElementById("sliderValues12");
  let sliderValueMin1 = document.getElementById("sliderValuesMin12");

  sliderOptMax.addEventListener("input", function () {
    sliderValueMax1.textContent = sliderOptMax.value;
    sliderValueMin1.textContent = sliderOptMin.value;
    //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });

  sliderOptMin.addEventListener("input", function () {
    sliderValueMin1.textContent = sliderOptMin.value;
    sliderValueMax1.textContent = sliderOptMax.value;
   //console.log("MBG slider row update is " ,document.getElementById("mbjgtbox").value, document.getElementById("mbjgtbox_l").value);
  });
}







//NEW TABLE WITH ROWUPDATES
function applySliderFilterTable(rowUpdate) {
  let mbgValue = mbgSlider();
  for (j = 0; j < rowUpdate.length; j++) {
    if (j[9] <= rowMbg) {
    }
    var row = table.insertRow(-1);
    var tmp_now = rowUpdate[j];

    for (k = 0; k < tmp_now.length ; k++) {
      var cell = row.insertCell(k);
      cell.innerHTML = tmp_now[k];
    }
  }
}

//ADD EVENT LISTENERS TO INPUTS
optSlider()
formationSlider();

