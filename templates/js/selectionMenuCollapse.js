function showSelectionOptionsButtons() {
  [
    "button-for-showing-sort-option",
    "button-for-showing-columns",
    "button-for-filter-by-tags",
    "button-for-filter-by-features",
    "button-for-filter-by-tags-and-features",
  ].forEach((x) => (document.getElementById(x).style.display = "inline-block"));
}

let closeableMenus = [
  "sortByRow",
  "columnSelectionHeadingRow",
  "columnSelectionRow",
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
    showSelectionOptionsButtons();
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
    showSelectionOptionsButtons();
    this.style.display = "none";
    document.getElementById("sortByRow").style.display = "flex";
  };

document.getElementById("button-for-showing-columns").onclick = function () {
  closeMenus();
  showSelectionOptionsButtons();
  this.style.display = "none";
  document.getElementById("columnSelectionHeadingRow").style.display = "flex";
  document.getElementById("columnSelectionRow").style.display = "flex";
};

document.getElementById("button-for-filter-by-tags").onclick = function () {
  closeMenus();
  showSelectionOptionsButtons();
  this.style.display = "none";
  document.getElementById("tagSelectionHeadingRow").style.display = "flex";
  document.getElementById("tagSelectionRow").style.display = "flex";
};

document.getElementById("button-for-filter-by-features").onclick = function () {
  closeMenus();
  showSelectionOptionsButtons();
  this.style.display = "none";
  document.getElementById("featureSelectionHeadingRow").style.display = "flex";
  document.getElementById("featureSelectionRow").style.display = "flex";
};

document.getElementById("button-for-filter-by-tags-and-features").onclick =
  function () {
    closeMenus();
    showSelectionOptionsButtons();
    this.style.display = "none";
    document.getElementById("tagSelectionHeadingRow").style.display = "flex";
    document.getElementById("tagSelectionRow").style.display = "flex";
    document.getElementById("featureSelectionHeadingRow").style.display =
      "flex";
    document.getElementById("featureSelectionRow").style.display = "flex";
  };
