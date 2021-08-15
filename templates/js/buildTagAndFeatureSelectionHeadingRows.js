// called from buildTagAndFeatureSelectionDivs.js
function buildTagSelectionHeadingRow(eParent, tagSortBy, dState) {
  let tagSelectionHeadingRow = document.createElement("div");
  tagSelectionHeadingRow.id = "tagSelectionHeadingRow";
  tagSelectionHeadingRow.style.maxWidth = "100%";
  tagSelectionHeadingRow.style.display = dState.tagSelectionHeadingRow;
  tagSelectionHeadingRow.style.justifyContent = "space-around";
  tagSelectionHeadingRow.style.alignItems = "center";

  let tagSelectionHeading = document.createElement("h2");
  tagSelectionHeading.innerHTML = "Select Tags";

  let tagSortByNameInputButton = buildRadioButton(
    (inputID = "tagSortByName"),
    (inputName = "tagSortBy"),
    (inputValue = "tagSortByName"),
    (sortedBy = tagSortBy),
    (sortedBySelector = "name"),
    (labelText = "Name")
  );

  let tagSortByNumThemesInputButton = buildRadioButton(
    (inputID = "tagSortByNumThemes"),
    (inputName = "tagSortBy"),
    (inputValue = "tagSortByNumThemes"),
    (sortedBy = tagSortBy),
    (sortedBySelector = "numThemes"),
    (labelText = "nThemes")
  );

  tagSelectionHeadingRow.appendChild(tagSelectionHeading);
  tagSelectionHeadingRow.appendChild(tagSortByNameInputButton);
  tagSelectionHeadingRow.appendChild(tagSortByNumThemesInputButton);
  eParent.appendChild(tagSelectionHeadingRow);

  let tagSortByNameInput = document.getElementById("tagSortByName");
  tagSortByNameInputButton.onclick = function () {
    if (!tagSortByNameInput.checked) {
      tagSortByNameInput.checked = true;
      buildResults();
    }
  };

  let tagSortByNumThemesInput = document.getElementById("tagSortByNumThemes");
  tagSortByNumThemesInputButton.onclick = function () {
    if (!tagSortByNumThemesInput.checked) {
      tagSortByNumThemesInput.checked = true;
      buildResults();
    }
  };
}

// called from buildTagAndFeatureSelectionDivs.js
function buildFeatureSelectionHeadingRow(eParent, featureSortBy, dState) {
  let featureSelectionHeadingRow = document.createElement("div");
  featureSelectionHeadingRow.id = "featureSelectionHeadingRow";
  featureSelectionHeadingRow.style.maxWidth = "100%";
  featureSelectionHeadingRow.style.display = dState.featureSelectionHeadingRow;
  featureSelectionHeadingRow.style.justifyContent = "space-around";
  featureSelectionHeadingRow.style.alignItems = "center";

  let featureSelectionHeading = document.createElement("h2");
  featureSelectionHeading.innerHTML = "Select Features";

  let featureSortByNameInputButton = buildRadioButton(
    (inputID = "featureSortByName"),
    (inputName = "featureSortBy"),
    (inputValue = "featureSortByName"),
    (sortedBy = featureSortBy),
    (sortedBySelector = "name"),
    (labelText = "Name")
  );

  let featureSortByNumThemesInputButton = buildRadioButton(
    (inputID = "featureSortByNumThemes"),
    (inputName = "featureSortBy"),
    (inputValue = "featureSortByNumThemes"),
    (sortedBy = featureSortBy),
    (sortedBySelector = "numThemes"),
    (labelText = "nThemes")
  );

  featureSelectionHeadingRow.appendChild(featureSelectionHeading);
  featureSelectionHeadingRow.appendChild(featureSortByNameInputButton);
  featureSelectionHeadingRow.appendChild(featureSortByNumThemesInputButton);
  eParent.appendChild(featureSelectionHeadingRow);

  let featureSortByNameInput = document.getElementById("featureSortByName");
  featureSortByNameInputButton.onclick = function () {
    if (!featureSortByNameInput.checked) {
      featureSortByNameInput.checked = true;
      buildResults();
    }
  };

  let featureSortByNumThemesInput = document.getElementById(
    "featureSortByNumThemes"
  );
  featureSortByNumThemesInputButton.onclick = function () {
    if (!featureSortByNumThemesInput.checked) {
      featureSortByNumThemesInput.checked = true;
      buildResults();
    }
  };
}
