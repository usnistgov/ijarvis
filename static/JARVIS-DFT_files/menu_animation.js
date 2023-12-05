//Navigation Menu
const press_menu_button = document.getElementById("press_button");
const display_menu = document.getElementById("menu_list");
const move_intro_section = document.getElementById("intro_section");

//Animation Function on Pressing menu
press_menu_button.addEventListener("click", function pressButton() {
  if (display_menu.style.display != "flex") {
    display_menu.style.display = "flex";
    move_intro_section.classList.add("jumbo_section_move_down");
    press_menu_button.src = "/static/images/menu-cancel.svg"; // src = https://img.icons8.com/ios-filled/344/ffffff/cancel.png
  } else {
    display_menu.style.display = "none";
    move_intro_section.classList.remove("jumbo_section_move_down");
    press_menu_button.src = "/static/images/menu-icon.svg";
  }
});
