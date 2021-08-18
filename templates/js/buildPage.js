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

function getSelected(filterCategory) {
  let selectionInputs = document.getElementsByClassName(
    `${filterCategory}SelectionInput`
  );
  if (selectionInputs.length > 0) {
    return [...selectionInputs].filter((x) => x.checked).map((y) => y.value);
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

function getTagAndFeatureFilteredThemes(selectedTags, selectedFeatures) {
  if (selectedTags.length === 0 && selectedFeatures.length === 0) {
    return themes;
  } else {
    return themes
      .filter((x) => selectedTags.every((y) => x.tags.includes(y)))
      .filter((z) => selectedFeatures.every((w) => z.features.includes(w)));
  }
}

function getFilteredThemes(tagAndFeatureFilteredThemes, selectedLicenses) {
  if (selectedLicenses.length === 0) {
    return tagAndFeatureFilteredThemes;
  } else {
    return tagAndFeatureFilteredThemes.filter((x) =>
      selectedLicenses.includes(x.license)
    );
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
    "licenseSelectionHeadingRow",
    "licenseSelectionRow",
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

  let selectedTags = getSelected("tag");
  let selectedFeatures = getSelected("feature");
  let selectedLicenses = getSelected("license");
  let sortedBy = getSortBy();
  let tagAndFeatureFilteredThemes = getTagAndFeatureFilteredThemes(
    selectedTags,
    selectedFeatures
  );
  let filtered_themes = getFilteredThemes(
    tagAndFeatureFilteredThemes,
    selectedLicenses
  );
  sortThemes(filtered_themes, sortedBy);
  filtered_themes.forEach((theme) => addThemeTableRow(theme, selectedColumns));

  // from buildSelectionMenu.js
  buildSelectionMenu(
    tagAndFeatureFilteredThemes,
    filtered_themes,
    sortedBy,
    selectedTags,
    selectedFeatures,
    selectedLicenses,
    selectedColumns,
    getDiplayState()
  );
}

buildResults();
