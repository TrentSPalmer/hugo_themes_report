function getMenuSortBy(sortBySelector) {
  let sortByNumThemes = document.getElementById(
    `${sortBySelector}SortByNumThemes`
  );
  if (sortByNumThemes === null) {
    return "numThemes";
  } else {
    return sortByNumThemes.checked ? "numThemes" : "name";
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
      // from buildSelectionInput.js
      buildInput(y, true, columnSelectionRow);
    });

  tableColumns
    .filter((x) => !selectedColumns.includes(x.headingName))
    .forEach((y) => {
      // from buildSelectionInput.js
      buildInput(y, false, columnSelectionRow);
    });
}

// called from buildPage.js
function buildSelectionMenu(
  tagAndFeatureFilteredThemes,
  sorted_themes,
  sortBy,
  selectedTags,
  selectedFeatures,
  selectedLicenses,
  selectedColumns,
  selectedMinVer,
  dState
) {
  let tagSortBy = getMenuSortBy("tag");
  let featureSortBy = getMenuSortBy("feature");
  let licenseSortBy = getMenuSortBy("license");
  let selectionMenuDiv = document.getElementById("selection-menu");

  // from getAvailableTagsAndFeaturesAndLicenses.js
  let availableTags = getAvailableTags(sorted_themes, tagSortBy);
  // from getAvailableTagsAndFeaturesAndLicenses.js
  let availableFeatures = getAvailableFeatures(sorted_themes, featureSortBy);
  // from getAvailableTagsAndFeaturesAndLicenses.js
  let availableLicences = getAvailableLicenses(
    tagAndFeatureFilteredThemes,
    licenseSortBy
  );

  // from buildSortByDiv.js
  buildSortByDiv(sortBy, dState.sortByRow);

  buildColumnSelectionDiv(selectedColumns, dState, selectionMenuDiv);

  buildMinVerSelectionDiv(selectedMinVer, dState, selectionMenuDiv);

  // from buildSelectionDivs.js
  buildSelectionDiv(
    selectedLicenses,
    availableLicences,
    licenseSortBy,
    dState.licenseSelectionRow,
    dState.licenseSelectionHeadingRow,
    selectionMenuDiv,
    "license"
  );

  // from buildSelectionDivs.js
  buildSelectionDiv(
    selectedTags,
    availableTags,
    tagSortBy,
    dState.tagSelectionRow,
    dState.tagSelectionHeadingRow,
    selectionMenuDiv,
    "tag"
  );

  // from buildSelectionDivs.js
  buildSelectionDiv(
    selectedFeatures,
    availableFeatures,
    featureSortBy,
    dState.featureSelectionRow,
    dState.featureSelectionHeadingRow,
    selectionMenuDiv,
    "feature"
  );
}
