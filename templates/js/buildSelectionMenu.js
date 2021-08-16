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

function buildColumnSelectionHeadingRow(eParent, dState) {
  let columnSelectionHeadingRow = document.createElement("div");
  columnSelectionHeadingRow.id = "columnSelectionHeadingRow";
  columnSelectionHeadingRow.style.maxWidth = "100%";
  columnSelectionHeadingRow.style.display = dState.columnSelectionHeadingRow;
  columnSelectionHeadingRow.style.alignItems = "center";

  let columnSelectionHeading = document.createElement("h2");
  columnSelectionHeading.innerHTML = "Select Columns";
  columnSelectionHeadingRow.appendChild(columnSelectionHeading);
  eParent.appendChild(columnSelectionHeadingRow);
}

function buildColumnSelectionDiv(selectedColumns, dState, eParent) {
  buildColumnSelectionHeadingRow(eParent, dState);

  let columnSelectionRow = document.createElement("div");
  columnSelectionRow.id = "columnSelectionRow";
  columnSelectionRow.style.display = dState.columnSelectionRow;
  columnSelectionRow.style.flexWrap = "wrap";
  columnSelectionRow.style.justifyContent = "space-around";
  eParent.appendChild(columnSelectionRow);

  tableColumns
    .filter((x) => selectedColumns.includes(x.headingName))
    .forEach((y) => {
      buildInput(y, true, columnSelectionRow);
    });

  tableColumns
    .filter((x) => !selectedColumns.includes(x.headingName))
    .forEach((y) => {
      buildInput(y, false, columnSelectionRow);
    });
}

// called from buildPage.js
function buildSelectionMenu(
  sorted_themes,
  sortBy,
  selectedTags,
  selectedFeatures,
  selectedColumns,
  dState
) {
  let tagSortBy = getTagSortBy();
  let featureSortBy = getFeatureSortBy();
  let selectionMenuDiv = document.getElementById("selection-menu");

  // from getAvailableTagsAndFeatures.js
  let availableTags = getAvailableTags(sorted_themes, tagSortBy);
  // from getAvailableTagsAndFeatures.js
  let availableFeatures = getAvailableFeatures(sorted_themes, featureSortBy);

  // from buildSortByDiv.js
  buildSortByDiv((sortedBy = sortBy), (sortByRowDisplay = dState.sortByRow));

  buildColumnSelectionDiv(
    (selectedColumns = selectedColumns),
    (dState = dState),
    (eParent = selectionMenuDiv)
  );

  // from buildTagAndFeatureSelectionDivs.js
  buildTagSelectionDiv(
    (selectedTags = selectedTags),
    (availableTags = availableTags),
    (tagSortBy = tagSortBy),
    (dState = dState),
    (eParent = selectionMenuDiv)
  );

  // from buildTagAndFeatureSelectionDivs.js
  buildFeatureSelectionDiv(
    (selectedFeatures = selectedFeatures),
    (availableFeatures = availableFeatures),
    (featureSortBy = featureSortBy),
    (dState = dState),
    (eParent = selectionMenuDiv)
  );
}
