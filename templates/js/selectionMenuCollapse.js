var menuButton = document.getElementById("selection-button");

menuButton.addEventListener("click", function () {
  menuButton.classList.toggle("active");
  var selectionMenu = document.getElementById("selection-menu");
  if (selectionMenu.style.display === "block") {
    selectionMenu.style.display = "none";
  } else {
    selectionMenu.style.display = "block";
  }
});
