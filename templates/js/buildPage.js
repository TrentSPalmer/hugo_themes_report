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

function getTagAndFeatureFilteredThemes(
  minVerFilteredThemes,
  selectedTags,
  selectedFeatures
) {
  if (selectedTags.length === 0 && selectedFeatures.length === 0) {
    return minVerFilteredThemes;
  } else {
    return minVerFilteredThemes
      .filter((x) => selectedTags.every((y) => x.tags.includes(y)))
      .filter((z) => selectedFeatures.every((w) => z.features.includes(w)));
  }
}

function getMinVerFilteredThemes(selectedMinVer) {
  if (selectedMinVer.length === 0 || selectedMinVer[0] === "none") {
    return themes;
  } else {
    // return licenseFilteredThemes;
    return themes
      .filter((x) => x.min_ver !== "")
      .filter((x) => semVerCompare(x.min_ver, selectedMinVer[0]) > -1);
  }
}

function getLicenseFilteredThemes(
  tagAndFeatureFilteredThemes,
  selectedLicenses
) {
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
    "minVerSelectionHeadingRow",
    "minVerSelectionRow",
    "tagSelectionHeadingRow",
    "tagSelectionRow",
    "featureSelectionHeadingRow",
    "featureSelectionRow",
    "minVerSelectionHeadingRow",
    "minVerSelectionRow",
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
  let selectedMinVer = getSelected("minVerRadioButton");
  let sortedBy = getSortBy();
  let minVerFilteredThemes = getMinVerFilteredThemes(selectedMinVer);
  let tagAndFeatureFilteredThemes = getTagAndFeatureFilteredThemes(
    minVerFilteredThemes,
    selectedTags,
    selectedFeatures
  );
  let filteredThemes = getLicenseFilteredThemes(
    tagAndFeatureFilteredThemes,
    selectedLicenses
  );
  sortThemes(filteredThemes, sortedBy);
  filteredThemes.forEach((theme) => addThemeTableRow(theme, selectedColumns));

  // from buildSelectionMenu.js
  buildSelectionMenu(
    tagAndFeatureFilteredThemes,
    filteredThemes,
    sortedBy,
    selectedTags,
    selectedFeatures,
    selectedLicenses,
    selectedColumns,
    selectedMinVer,
    getDiplayState()
  );
}

buildResults();
