function getSortBy() {
  let a = document.getElementsByClassName("sortBy");
  if (a.length > 0) {
    return [
      ...[...a].filter((y) => y.checked).map((x) => x.value),
      ...[...a].filter((y) => !y.checked).map((x) => x.value),
    ];
  } else {
    return ["date", "stars", "name", "minVer", "license"];
  }
}

function getSelectedTags() {
  let tagSelectionInputs = document.getElementsByClassName("tagSelectionInput");
  if (tagSelectionInputs.length > 0) {
    return [...tagSelectionInputs].filter((x) => x.checked).map((y) => y.value);
  } else {
    return [];
  }
}

function getSelectedColumns() {
  let columnSelectionInputs = document.getElementsByClassName(
    "columnSelectionInput"
  );
  if (columnSelectionInputs.length > 0) {
    let checked = [...columnSelectionInputs].filter((x) => x.checked);
    if (checked.length > 0) {
      return checked.map((y) => y.id.slice(0, -23));
    } else {
      return ["cname", "date", "num_stars", "commit"];
    }
  } else {
    return ["cname", "date", "num_stars", "commit"];
  }
}

function getSelectedFeatures() {
  let featureSelectionInputs = document.getElementsByClassName(
    "featureSelectionInput"
  );
  if (featureSelectionInputs.length > 0) {
    return [...featureSelectionInputs]
      .filter((x) => x.checked)
      .map((y) => y.value);
  } else {
    return [];
  }
}

function getFilteredThemes(selectedTags, selectedFeatures) {
  if (selectedTags.length === 0 && selectedFeatures.length === 0) {
    return themes;
  } else {
    return themes
      .filter((x) => selectedTags.every((y) => x.tags.includes(y)))
      .filter((z) => selectedFeatures.every((w) => z.features.includes(w)));
  }
}

function getDState(x) {
  let e = document.getElementById(x);
  return e !== null ? e.style.display : "none";
}

function getDiplayState() {
  let dState = {};
  [
    "sortByRow",
    "columnSelectionHeadingRow",
    "columnSelectionRow",
    "tagSelectionHeadingRow",
    "tagSelectionRow",
    "featureSelectionHeadingRow",
    "featureSelectionRow",
  ].forEach((x) => (dState[x] = getDState(x)));
  return dState;
}

let tableColumns = [
  { headingName: "cname", headingText: "theme" },
  { headingName: "date", headingText: "date" },
  { headingName: "num_stars", headingText: "stars" },
  { headingName: "commit", headingText: "commit" },
  { headingName: "min_ver", headingText: "minVer" },
  { headingName: "license", headingText: "license" },
  { headingName: "desc", headingText: "desc" },
  { headingName: "tags", headingText: "tags" },
  { headingName: "features", headingText: "features" },
];

function buildResults() {
  let resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";
  let resultsTable = document.createElement("table");
  resultsTable.id = "resultsTable";
  resultsTable.style.border = "1px solid black";
  resultsTable.style.fontSize = ".9rem";

  let resultsTableHeadRow = document.createElement("tr");
  resultsDiv.appendChild(resultsTable);
  resultsTable.appendChild(resultsTableHeadRow);
  let selectedColumns = getSelectedColumns();

  tableColumns
    .filter((y) => selectedColumns.includes(y.headingName))
    .forEach((x) => {
      let xTH = document.createElement("th");
      xTH.innerHTML = x.headingText;
      resultsTableHeadRow.appendChild(xTH);
    });

  let selectedTags = getSelectedTags();
  let selectedFeatures = getSelectedFeatures();
  let sortedBy = getSortBy();
  // let filtered_themes = getFilteredThemes(selectedTags, selectedFeatures);
  let sorted_themes = getFilteredThemes(selectedTags, selectedFeatures);
  sortThemes(sorted_themes, sortedBy);
  sorted_themes.forEach((theme) => addThemeTableRow(theme, selectedColumns));

  // from buildSelectionMenu.js
  buildSelectionMenu(
    (sorted_themes = sorted_themes),
    (sortBy = sortedBy),
    (selectedTags = selectedTags),
    (selectedFeatures = selectedFeatures),
    (selectedColumns = selectedColumns),
    (dState = getDiplayState())
  );
}

buildResults();
