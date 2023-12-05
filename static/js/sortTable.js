//SORTING TABLE

//Get table
//store results in a list
let listOfItems = [];

//Sort Table function
function sortTable(n) {
  var table,
    rows,
    switching,
    i,
    currentCellX,
    currentCellY,
    switchNow,
    direction,
    switchCount = 0;

  //get table
  table = document.getElementById("table-sort");
  switching = true;
  //Set the sorting direction to ascending:
  direction = "asc";
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < rows.length - 1; i++) {
      //start by saying there should be no switching:
      switchNow = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      currentCellX = rows[i].getElementsByTagName("TD")[n];
      currentCellY = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (direction == "asc") {
        if (
          currentCellX.textContent.toLowerCase() >
          currentCellY.textContent.toLowerCase()
        ) {
          //if so, mark as a switch and break the loop:
          switchNow = true;
          break;
        }
      } else if (direction == "desc") {
        if (
          currentCellX.textContent.toLowerCase() <
          currentCellY.textContent.toLowerCase()
        ) {
          //if so, mark as a switch and break the loop:
          switchNow = true;
          break;
        }
      }
    }
    if (switchNow) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchCount++;
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchCount == 0 && direction == "asc") {
        direction = "desc";
        switching = true;
      }
    }
  }
}
