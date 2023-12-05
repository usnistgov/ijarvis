const content = document.getElementById("content");
const spinner = document.getElementById("page-loading");

// Change display none to flex
//Display content after 2 seconds
setTimeout(function () {
  content.style.display = "flex";
  spinner.style.display = "none";
}, 2000);
