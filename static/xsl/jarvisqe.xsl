<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">

<html> 
<head>
<style>
.jcentered {
  margin: auto;
  width: 95%;
 border: 1px solid black;
  padding: 1px;
}
.jright {
  position: absolute;
  right: 0px;
  width: 300px;
  border: 3px solid #73AD21;
  padding: 10px;
}
.jleft {
  position: absolute;
  left: 0px;
  width: 300px;
  border: 3px solid #73AD21;
  padding: 10px;

}

</style>
<script src="https://cdnjs.cloudflare.com/ajax/libs/3Dmol/1.4.0/3Dmol-min.js"></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"> </script>
 <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script> 


<!-- Bootstrap CSS START-->
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous" />

<script src="https://cdnjs.cloudflare.com/ajax/libs/mathjs/7.5.1/math.min.js" integrity="sha512-6SHRAV8GhJ+3WvGPKQNsBpLj7J9QF9JFwH7nPSRLtH/OqFrlXRd54Z+QDgw7xj1f7dV8c50sKhZYr/xGPlMoiw==" crossorigin="anonymous"></script>


</head>


<body>

<nav class="navbar navbar-expand-lg navbar-light" style="background-color: #00bfff;">

  <div class="collapse navbar-collapse" >

    <ul class="nav navbar-nav">
    <a class="nav-link active"  href="https://jarvis.nist.gov/">JARVIS API</a>
    <a class="nav-link active"  href="https://jarvis.nist.gov/jarvisdft/">JARVIS-DFT</a>
    <a class="nav-link active"  href="https://jarvis.nist.gov/jarvisff/">JARVIS-FF</a>
    <a class="nav-link active"  href="https://jarvis.nist.gov/jarvisml/">JARVIS-ML</a>
    <a class="nav-link active"  href="https://github.com/usnistgov/jarvis">JARVIS-Tools</a>
    <a class="nav-link active"  href="https://jarvis-materials-design.github.io/dbdocs/jarvisdft/#property-details">Documentation</a>
    <a class="nav-link active"  href="https://jarvis-materials-design.github.io/dbdocs/publications/">Publications</a>
    <a class="nav-link active"  href="https://jarvis.nist.gov/contact">Report bug/Contact</a>

    </ul>
  </div>
</nav>



  
<!-- Basic table start -->
  <table class="jcentered table  btn-table" >

 
    <tr>
      <td>ID: <xsl:value-of select="basic_info/jid"/></td>
      <td>functional: <xsl:value-of select="basic_info/functional"/></td>
      <td>Input cell</td>
      <td>Input cell</td>
      <td>Number of species: <xsl:value-of select="basic_info/number_uniq_species"/></td>
     
    </tr>
    <tr>
      <td>Chemical formula: <xsl:value-of select="basic_info/formula"/></td>
      <td>PSP: GBRV</td>
      <td>a: <xsl:value-of select="basic_info/final_a"/> &#8491;</td>
      <td>&#945;: <xsl:value-of select="basic_info/final_alpha"/> &#176;</td>
      <td>Nelec: <xsl:value-of select="basic_info/nelec"/> </td>
     
    </tr>
    <tr>
      <td>Space-group: <xsl:value-of select="basic_info/final_spacegroup_symbol"/></td>
      <td>Bandgap (eV): <xsl:value-of select="basic_info/indir_gap"/></td>
      <td>b: <xsl:value-of select="basic_info/final_b"/> &#8491;</td>
      <td>&#946;: <xsl:value-of select="basic_info/final_beta"/> &#176;</td>
      <td>Efermi (eV): <xsl:value-of select="basic_info/efermi"/> </td>
      
    </tr>
    <tr>
      <td>Crystal system: <xsl:value-of select="basic_info/final_crystal_system"/></td>
      <td>Form. energy/atom (eV): <xsl:value-of select="basic_info/f_enp"/></td>
      
      <td>c: <xsl:value-of select="basic_info/final_c"/> &#8491;</td>
      <td>&#947;: <xsl:value-of select="basic_info/final_gamma"/> &#176;</td>
      <td>NKpts: <xsl:value-of select="basic_info/nkpts"/> </td>
      
    </tr>
    <tr>
      <td>Data source: <xsl:value-of select="basic_info/data_source"/></td>
      <td>Energy/atom (eV): <xsl:value-of select="basic_info/energy_per_atom"/></td>

      <td>Density (gcm<sup>-3</sup>): <xsl:value-of select="basic_info/final_density"/></td>
      <td>Spin-polarized: <xsl:value-of select="basic_info/is_spin_polarized"/></td>
      <td>Spin-orbit: <xsl:value-of select="basic_info/is_spin_polarized"/></td>
    
    </tr>    
   
   
    




 
    
   
  </table>
  
  
<!-- Basic table end -->
<br></br>


<!--contcar starts-->
<textarea  rows="15" cols="50" style="display:none" id="contcar">
</textarea>
<script>
function Function_contcar() {

  var x=<xsl:value-of select="basic_info/final_structure"/>;
  document.getElementById("contcar").style.display = 'block';
  document.getElementById("contcar").value = (x);
}
</script>
<button type="button" class="btn btn-primary" onclick="Function_contcar()">Show POSCAR</button>


<!--contcar ends-->

 <!--xyz starts-->


<button type="button" class="btn btn-primary" onclick="Function_cif()">Show CIF format</button>
<script>
function Function_cif() {

  var x=<xsl:value-of select="basic_info/cif"/>;
  document.getElementById("contcar").style.display = 'block';
  document.getElementById("contcar").value = (x);
}
</script>
<!--xyz ends-->

<!-- Structure viewer start -->
<h3 style="text-align:center">Visualizing atomic structure</h3>
  <div >

  <div 
  class="jcentered"
  id="geometry"
  style="height: 400px; width: 400px; position: relative;"
  data-backgroundcolor="0xffffff"
  >  
  <span
    style="
      display: inline-block;
      z-index: 1;
      position: absolute;
      bottom: 0px;
      right: 0px;
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    "
    >
    
    </span>
  </div>

  
  

<script>
  var data =
    <xsl:value-of select="basic_info/xyz"/>;
  var viewer = $3Dmol.createViewer("geometry", {
    backgroundColor: "white",
  });
 // viewer.setStyle({stick:{colorscheme:"Jmol"}});
  
  viewer.addModel(data, "xyz");
  viewer.setStyle({ sphere: { radius: 0.7 } });
  
  viewer.addStyle({ stick: { radius: 0.2 } });
  viewer.zoomTo();
  viewer.setClickable({},true,function(atom,viewer,event,container) {
                       viewer.addLabel(atom.resn+":"+atom.atom,{position: atom, backgroundColor: 'darkgreen', backgroundOpacity: 0.8});
                   });
 
  viewer.render();
</script>


  </div>
 <!-- Structure viewer end -->


 <!--DOS start-->

<script>
    
  var x= <xsl:value-of select="basic_info/dos/edos_energies"/>;
  
  if (x!==''){

   var header = document.createElement("h3");
   header.className="jcentered";
   var text = document.createTextNode("Electronic density of states");
    header.appendChild(text);
    header.style.textAlign='center';
    document.body.appendChild(header);


    var divElement = document.createElement("div");
    divElement.id = "dos";
    divElement.setAttribute('class', 'jcentered');
    document.body.appendChild(divElement);

    };


</script>
<script>
function dos_plotly(){
//  var data=[];
//var data = [data1,data1a];
//var data = [data1,data1a, data2,data2a, data3,data3a,data3b,data3c];
var plot_font = 14;
var layout_convg = {
  grid: {rows: 1, columns: 2},
  xaxis1: {visible:'legendonly',domain: [0.1, 0.4],tickfont: {size: plot_font,color:'black'},title:{text: 'E-Ef (eV)',font:{size: plot_font,color:"black"}}},

  xaxis2: {visible:'legendonly',domain: [0.4, 0.8],tickfont: {size: plot_font,color:'black'},title:{text: 'E-Ef (eV)',font:{size: plot_font,color:"black"}}},
  //xaxis3: {domain: [0.66, 0.99],tickfont: {size: plot_font,color:'black'},title:{text: 'E-Ef (eV)',font:{size: plot_font,color:"black"}}},

  //title:str1.join(cnvg_kp.toString()).join(str2).join(cnvg_enc.toString()),

  showlegend: true,
  autosize: false,

  width:1200,

      yaxis1: {
    showlegend: false,
     title:{text: 'DOS (1/eV)',font:{size: plot_font,color:"black"}},

   },
     xaxis1: {
     range: [-10, 10],
     title:{text: 'E-E<sub>f</sub> (eV) (Total DOS)',font:{size: plot_font,color:"black"}},
     
   },
      xaxis2: {
     range: [-10, 10],
     showlegend: true,
     title:{text: 'E-E<sub>f</sub>(eV) (Atom Proj. DOS)',font:{size: plot_font,color:"black"}},
     autorange: false,
   },

};
Plotly.newPlot('dos', data, layout_convg,{displaylogo: false});

};
   var data=[]

  var x1= <xsl:value-of select="basic_info/dos/edos_energies"/>;
  x1=x1.split(',').map(Number);
  
  var y1= <xsl:value-of select="basic_info/dos/total_edos_up"/>;
  y1=y1.split(',').map(Number);
  var y1a= <xsl:value-of select="basic_info/dos/total_edos_up"/>;
  y1a=y1a.split(',').map(Number);

  var data1 = {
    x: x1 ,
    y: y1,
    xaxis: "x1",
    yaxis: "y1",
    type: "scatter",
    "name":"Total DOS",
  };

    var data1a = {
    x: x1 ,
    y: y1a,
    xaxis: "x1",
    yaxis: "y1a",
    type: "scatter",
    "name":"Total DOS",
  };
   data.push(data1);
   

 
 
 
 
   var x2= <xsl:value-of select="basic_info/dos/edos_energies"/>;
  x2=x2.split(',').map(Number);
  var y2= <xsl:value-of select="basic_info/dos/elemental_dos"/>;
  //console.log(y2);
  y2=y2.split(';');
  
 for (var i=0;i&lt;y2.length-1;i++) {

  var data2 = {
    x: x2,
    y: y2[i].split('_')[1].split(',').map(Number),
    xaxis: "x2",
   
    type: "scatter",
    name: y2[i].split('_')[0],
  };


 data.push(data2);
};


  dos_plotly();
</script>

<!--DOS end-->
  <br></br>

 

<!--Force tensor table starts-->



  <script>
  var x= <xsl:value-of select="basic_info/forces"/>;
  if (x!==''){

   var header = document.createElement("h3");
   header.className="jcentered";
   var text = document.createTextNode("Forces");
    header.appendChild(text);
    header.style.textAlign='center';
    document.body.appendChild(header);


     var divElement = document.createElement("table");
    divElement.id = "elastic_tensor";
    divElement.setAttribute('class', 'jcentered');
    document.body.appendChild(divElement);

    };
</script>

<script>
 var table = document.getElementById("elastic_tensor");
 document.getElementById("elastic_tensor").style.height = "500px"
  
 elasticij=<xsl:value-of select="basic_info/forces"/> ;
 elasticij=elasticij.split(',');
 //console.log('elasticij',elasticij.length);
 var arr=[];
 
  for (var i=0;i&lt;elasticij.length;i++) {


 arr.push(i+1);
 };
 
 arr=[arr];
 var row = table.insertRow(-1);
 var count=0;
 var tmp=[];
 
 var xx=[]
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[0]);
 };
 arr.push(xx);
 
 var xx=[]
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[1]);
 }; 
  arr.push(xx);
  
 var xx=[] 
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[2]);
 };
 arr.push(xx);
//console.log('arr',arr);
 var data = [{   
  type: 'table',
 header:{values: ["#Atom","f<sub>x</sub> (eV&#8491;<sup>-1</sup>)","f<sub>y</sub> (eV&#8491;<sup>-1</sup>)","f<sub>z</sub> (eV&#8491;<sup>-1</sup>)"],height: 18,font: {family: "Arial", size: 24, color: ["black"]}},

  cells: {
    values: arr,
    align: "center",
    line: {color: "black", width: 1},
    font: {family: "Arial", size: 18, color: ["black"]},
    height: 25,
  }
}]



var layout = {
   xaxis1: {domain: [0.1, 0.2],},
   yaxis1: {domain: [0., 1.95],},

}

Plotly.newPlot('elastic_tensor',data);
</script>
<!--Force tensor table ends-->
<br></br>



  
  
<!--Stress tensor table starts-->



  <script>
  var x= <xsl:value-of select="basic_info/stress"/>;
  if (x!==''){

   var header = document.createElement("h3");
   header.className="jcentered";
  
   var text = document.createTextNode("Stress");
    header.appendChild(text);
    header.style.textAlign='center';
    document.body.appendChild(header);


     var divElement = document.createElement("table");
    divElement.id = "selastic_tensor";
    divElement.setAttribute('class', 'jcentered');
    document.body.appendChild(divElement);

    };
</script>

<script>
 var table = document.getElementById("selastic_tensor");
 elasticij=<xsl:value-of select="basic_info/stress"/> ;
 elasticij=elasticij.split(',');
 //console.log('elasticij',elasticij.length);
 var arr=[];

 
 arr=[["x","y","z"]];
 var row = table.insertRow(-1);
 var count=0;
 var tmp=[];
 
 var xx=[]
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[0]);
 };
 arr.push(xx);
 
 var xx=[]
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[1]);
 }; 
  arr.push(xx);
  
 var xx=[] 
 for (var i=0;i&lt;elasticij.length;i++) {
 tmp=math.round(elasticij[i].split(' ').map(Number),6);
 //console.log('tmp',tmp)
 xx.push(tmp[2]);
 };
 arr.push(xx);
//console.log('arr',arr);
 var data = [{
  type: 'table',
 header:{values: ["eV&#8491;<sup>-3</sup>","x","y","z"],height: 30,font: {family: "Arial", size: 24, color: ["black"]}},

  cells: {
    values: arr,
    align: "center",
    line: {color: "black", width: 1},
    font: {family: "Arial", size: 24, color: ["black"]},
    height: 30,
  }
}]



var layout = {
   xaxis1: {domain: [0.1, 0.4],},
   //xaxis2: {domain: [0.4, 0.95],},

}

Plotly.newPlot('selastic_tensor',data);
</script>
<!--Stress tensor table ends-->
<br></br>  
  
  
  
  
  
  
  


















</body>
</html>
</xsl:template>
</xsl:stylesheet>




