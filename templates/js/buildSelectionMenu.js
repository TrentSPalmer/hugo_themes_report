function buildTagSelectionHeadingRow(selectionMenuDiv, tagSortBy) {
  let tagSelectionHeadingRow = document.createElement("div");
  tagSelectionHeadingRow.id = "tagSelectionHeadingRow";
  tagSelectionHeadingRow.style.maxWidth = "100%";
  tagSelectionHeadingRow.style.display = "flex";
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
  selectionMenuDiv.appendChild(tagSelectionHeadingRow);

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

function buildFeatureSelectionHeadingRow(selectionMenuDiv, featureSortBy) {
  let featureSelectionHeadingRow = document.createElement("div");
  featureSelectionHeadingRow.id = "featureSelectionHeadingRow";
  featureSelectionHeadingRow.style.maxWidth = "100%";
  featureSelectionHeadingRow.style.display = "flex";
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
  selectionMenuDiv.appendChild(featureSelectionHeadingRow);

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

function buildTagSelectionDiv(selectedTags, availableTags, tagSortBy) {
  let selectionMenuDiv = document.getElementById("selection-menu");
  buildTagSelectionHeadingRow(selectionMenuDiv, tagSortBy);

  let tagSelectionRow = document.createElement("div");
  tagSelectionRow.style.display = "flex";
  tagSelectionRow.style.flexWrap = "wrap";
  tagSelectionRow.style.justifyContent = "space-around";

  selectionMenuDiv.appendChild(tagSelectionRow);

  availableTags
    .filter((x) => selectedTags.includes(x.tag))
    .forEach((y) => {
      buildTagSelectionInput(y, true, tagSelectionRow);
    });

  availableTags
    .filter((x) => !selectedTags.includes(x.tag))
    .forEach((y) => {
      buildTagSelectionInput(y, false, tagSelectionRow);
    });
}

function buildFeatureSelectionDiv(
  selectedFeatures,
  availableFeatures,
  featureSortBy
) {
  let selectionMenuDiv = document.getElementById("selection-menu");
  buildFeatureSelectionHeadingRow(selectionMenuDiv, featureSortBy);

  let featureSelectionRow = document.createElement("div");
  featureSelectionRow.style.display = "flex";
  featureSelectionRow.style.flexWrap = "wrap";
  featureSelectionRow.style.justifyContent = "space-around";

  selectionMenuDiv.appendChild(featureSelectionRow);

  availableFeatures
    .filter((x) => selectedFeatures.includes(x.feature))
    .forEach((y) => {
      buildFeatureSelectionInput(y, true, featureSelectionRow);
    });

  availableFeatures
    .filter((x) => !selectedFeatures.includes(x.feature))
    .forEach((y) => {
      buildFeatureSelectionInput(y, false, featureSelectionRow);
    });
}

function buildSelectionMenu(
  sorted_themes,
  sortedBy,
  selectedTags,
  selectedFeatures
) {
  let tagSortBy = getTagSortBy();
  let featureSortBy = getFeatureSortBy();
  let availableTags = getAvailableTags(sorted_themes, tagSortBy);
  let availableFeatures = getAvailableFeatures(sorted_themes, featureSortBy);
  buildSortByDiv(sortedBy);
  buildTagSelectionDiv(selectedTags, availableTags, tagSortBy);
  buildFeatureSelectionDiv(selectedFeatures, availableFeatures, featureSortBy);
}
