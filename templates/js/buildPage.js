function getSortBy() {
  let sortByLastCommitInput = document.getElementById("sortByDate");
  if (sortByLastCommitInput === null) {
    return "date";
  } else {
    return sortByLastCommitInput.checked ? "date" : "stars";
  }
}

function getTagSortBy() {
  let tagSortByNumThemes = document.getElementById("tagSortByNumThemes");
  if (tagSortByNumThemes === null) {
    return "numThemes";
  } else {
    return tagSortByNumThemes.checked ? "numThemes" : "name";
  }
}

function getFeatureSortBy() {
  let featureSortByNumThemes = document.getElementById(
    "featureSortByNumThemes"
  );
  if (featureSortByNumThemes === null) {
    return "numThemes";
  } else {
    return featureSortByNumThemes.checked ? "numThemes" : "name";
  }
}

function getSortedThemes(themeList, sortedBy) {
  if (sortedBy === "date") {
    return themeList.sort((a, b) => b.date_in_seconds - a.date_in_seconds);
  } else {
    return themeList.sort((a, b) => b.num_stars - a.num_stars);
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
    "tagSelectionHeadingRow",
    "tagSelectionRow",
    "featureSelectionHeadingRow",
    "featureSelectionRow",
  ].forEach((x) => (dState[x] = getDState(x)));
  return dState;
}

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

  let tableHeadingVals = [
    {'headingName': 'cname', 'headingText': 'theme'},
    {'headingName': 'date', 'headingText': 'date'},
    {'headingName': 'num_stars', 'headingText': 'stars'},
    {'headingName': 'commit', 'headingText': 'commit'},
    {'headingName': 'min_ver', 'headingText': 'minVer'},
    {'headingName': 'license', 'headingText': 'license'},
    {'headingName': 'desc', 'headingText': 'desc'},
    {'headingName': 'tags', 'headingText': 'tags'},
    {'headingName': 'features', 'headingText': 'features'},
  ];

  tableHeadingVals.forEach((x) => {
    let xTH = document.createElement("th");
    xTH.innerHTML = x.headingText;
    resultsTableHeadRow.appendChild(xTH);
  });

  let selectedTags = getSelectedTags();
  let selectedFeatures = getSelectedFeatures();
  let sortedBy = getSortBy();
  let filtered_themes = getFilteredThemes(selectedTags, selectedFeatures);
  let sorted_themes = getSortedThemes(filtered_themes, sortedBy);
  sorted_themes.forEach((theme) => addThemeTableRow(theme));

  buildSelectionMenu(
    sorted_themes,
    sortedBy,
    selectedTags,
    selectedFeatures,
    getDiplayState()
  );
}

buildResults();
