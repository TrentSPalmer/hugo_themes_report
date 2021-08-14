let closeableMenus = [
  "sortByRow",
  "tagSelectionHeadingRow",
  "tagSelectionRow",
  "featureSelectionHeadingRow",
  "featureSelectionRow",
];

let areAnyCloseAbleMenusOpen = () =>
  closeableMenus.some(
    (x) => document.getElementById(x).style.display !== "none"
  );

function closeMenus() {
  closeableMenus.forEach(
    (x) => (document.getElementById(x).style.display = "none")
  );
}

function closeOptionMenu() {
  document.getElementById("selection-options-menu").style.display = "none";
}

document.getElementById("plus-button").onclick = function () {
  this.style.display = "none";
  document.getElementById("minus-button").style.display = "inline-block";
  document.getElementById("selection-options-menu").style.display = "flex";
  closeMenus();
  window.scrollTo(0, 0);
};

document.getElementById("minus-button").onclick = function () {
  if (areAnyCloseAbleMenusOpen()) {
    closeMenus();
  } else {
    document.getElementById("selection-options-menu").style.display = "none";
    this.style.display = "none";
    document.getElementById("plus-button").style.display = "inline-block";
  }
  window.scrollTo(0, 0);
};

document.getElementById("button-for-showing-sort-option").onclick =
  function () {
    closeMenus();
    document.getElementById("sortByRow").style.display = "flex";
  };

document.getElementById("button-for-showing-columns").onclick = function () {};

document.getElementById("button-for-filter-by-tags").onclick = function () {
  closeMenus();
  document.getElementById("tagSelectionHeadingRow").style.display = "flex";
  document.getElementById("tagSelectionRow").style.display = "flex";
};

document.getElementById("button-for-filter-by-features").onclick = function () {
  closeMenus();
  document.getElementById("featureSelectionHeadingRow").style.display = "flex";
  document.getElementById("featureSelectionRow").style.display = "flex";
};

document.getElementById("button-for-filter-by-tags-and-features").onclick =
  function () {
    closeMenus();
    document.getElementById("tagSelectionHeadingRow").style.display = "flex";
    document.getElementById("tagSelectionRow").style.display = "flex";
    document.getElementById("featureSelectionHeadingRow").style.display =
      "flex";
    document.getElementById("featureSelectionRow").style.display = "flex";
  };
