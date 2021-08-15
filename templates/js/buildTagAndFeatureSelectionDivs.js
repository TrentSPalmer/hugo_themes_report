// called from buildSelectionMenu.js
function buildTagSelectionDiv(
  selectedTags,
  availableTags,
  tagSortBy,
  dState,
  eParent
) {
  // from buildTagAndFeatureSelectionHeadingRows.js
  buildTagSelectionHeadingRow(eParent, tagSortBy, dState);

  let tagSelectionRow = document.createElement("div");
  tagSelectionRow.id = "tagSelectionRow";
  tagSelectionRow.style.display = dState.tagSelectionRow;
  tagSelectionRow.style.flexWrap = "wrap";
  tagSelectionRow.style.justifyContent = "space-around";

  eParent.appendChild(tagSelectionRow);

  availableTags
    .filter((x) => selectedTags.includes(x.tag))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, true, tagSelectionRow);
    });

  availableTags
    .filter((x) => !selectedTags.includes(x.tag))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, false, tagSelectionRow);
    });
}

// called from buildSelectionMenu.js
function buildFeatureSelectionDiv(
  selectedFeatures,
  availableFeatures,
  featureSortBy,
  dState,
  eParent
) {
  // from buildTagAndFeatureSelectionHeadingRows.js
  buildFeatureSelectionHeadingRow(eParent, featureSortBy, dState);

  let featureSelectionRow = document.createElement("div");
  featureSelectionRow.id = "featureSelectionRow";
  featureSelectionRow.style.display = dState.featureSelectionRow;
  featureSelectionRow.style.flexWrap = "wrap";
  featureSelectionRow.style.justifyContent = "space-around";

  eParent.appendChild(featureSelectionRow);

  availableFeatures
    .filter((x) => selectedFeatures.includes(x.feature))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, true, featureSelectionRow);
    });

  availableFeatures
    .filter((x) => !selectedFeatures.includes(x.feature))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, false, featureSelectionRow);
    });
}
