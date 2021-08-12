function buildTagSelectionHeadingRow(selectionMenuDiv, tagSortBy) {
  let tagSelectionHeadingRow = document.createElement('div');
  tagSelectionHeadingRow.id = 'tagSelectionHeadingRow';
  tagSelectionHeadingRow.style.maxWidth = '100%';
  tagSelectionHeadingRow.style.display = 'flex';
  tagSelectionHeadingRow.style.justifyContent = 'space-around';

  let tagSelectionHeading = document.createElement('h2');
  tagSelectionHeading.innerHTML = "Select Tags";

  let tagSortByNameInputDiv = document.createElement('div');
  tagSortByNameInputDiv.style.display = 'flex';
  tagSortByNameInputDiv.style.alignItems = 'center';
  let tagSortByNameInput = document.createElement('input');
  tagSortByNameInput.type = 'radio';
  tagSortByNameInput.id = 'tagSortByName';
  tagSortByNameInput.name = 'tagSortBy';
  tagSortByNameInput.value = 'tagSortByName';
  tagSortByNameInput.checked = tagSortBy === 'name' ? true : false;
  tagSortByNameInput.onclick = function() { buildResults(); };
  tagSortByNameInputDiv.appendChild(tagSortByNameInput);

  let tagSortByNameInputLabel = document.createElement('label');
  tagSortByNameInputLabel.for = 'tagSortByName';
  tagSortByNameInputLabel.innerHTML = 'Name';
  tagSortByNameInputDiv.appendChild(tagSortByNameInputLabel);

  let tagSortByNumThemesInputDiv = document.createElement('div');
  tagSortByNumThemesInputDiv.style.display = 'flex';
  tagSortByNumThemesInputDiv.style.alignItems = 'center';
  let tagSortByNumThemesInput = document.createElement('input');
  tagSortByNumThemesInput.type = 'radio';
  tagSortByNumThemesInput.id = 'tagSortByNumThemes';
  tagSortByNumThemesInput.name = 'tagSortBy';
  tagSortByNumThemesInput.value = 'tagSortByNumThemes';
  tagSortByNumThemesInput.checked = tagSortBy === 'numThemes' ? true : false;
  tagSortByNumThemesInput.onclick = function() { buildResults(); };
  tagSortByNumThemesInputDiv.appendChild(tagSortByNumThemesInput);

  let tagSortByNumThemesInputLabel = document.createElement('label');
  tagSortByNumThemesInputLabel.for = 'tagSortByNumThemes';
  tagSortByNumThemesInputLabel.innerHTML = 'numThemes';
  tagSortByNumThemesInputDiv.appendChild(tagSortByNumThemesInputLabel);

  tagSelectionHeadingRow.appendChild(tagSelectionHeading);
  tagSelectionHeadingRow.appendChild(tagSortByNameInputDiv);
  tagSelectionHeadingRow.appendChild(tagSortByNumThemesInputDiv);
  selectionMenuDiv.appendChild(tagSelectionHeadingRow);
}

function buildFeatureSelectionHeadingRow(selectionMenuDiv, featureSortBy) {
  let featureSelectionHeadingRow = document.createElement('div');
  featureSelectionHeadingRow.id = 'featureSelectionHeadingRow';
  featureSelectionHeadingRow.style.maxWidth = '100%';
  featureSelectionHeadingRow.style.display = 'flex';
  featureSelectionHeadingRow.style.justifyContent = 'space-around';

  let featureSelectionHeading = document.createElement('h2');
  featureSelectionHeading.innerHTML = "Select Features";

  let featureSortByNameInputDiv = document.createElement('div');
  featureSortByNameInputDiv.style.display = 'flex';
  featureSortByNameInputDiv.style.alignItems = 'center';
  let featureSortByNameInput = document.createElement('input');
  featureSortByNameInput.type = 'radio';
  featureSortByNameInput.id = 'featureSortByName';
  featureSortByNameInput.name = 'featureSortBy';
  featureSortByNameInput.value = 'featureSortByName';
  featureSortByNameInput.checked = featureSortBy === 'name' ? true : false;
  featureSortByNameInput.onclick = function() { buildResults(); };
  featureSortByNameInputDiv.appendChild(featureSortByNameInput);

  let featureSortByNameInputLabel = document.createElement('label');
  featureSortByNameInputLabel.for = 'featureSortByName';
  featureSortByNameInputLabel.innerHTML = 'Name';
  featureSortByNameInputDiv.appendChild(featureSortByNameInputLabel);

  let featureSortByNumThemesInputDiv = document.createElement('div');
  featureSortByNumThemesInputDiv.style.display = 'flex';
  featureSortByNumThemesInputDiv.style.alignItems = 'center';
  let featureSortByNumThemesInput = document.createElement('input');
  featureSortByNumThemesInput.type = 'radio';
  featureSortByNumThemesInput.id = 'featureSortByNumThemes';
  featureSortByNumThemesInput.name = 'featureSortBy';
  featureSortByNumThemesInput.value = 'featureSortByNumThemes';
  featureSortByNumThemesInput.checked = featureSortBy === 'numThemes' ? true : false;
  featureSortByNumThemesInput.onclick = function() { buildResults(); };
  featureSortByNumThemesInputDiv.appendChild(featureSortByNumThemesInput);

  let featureSortByNumThemesInputLabel = document.createElement('label');
  featureSortByNumThemesInputLabel.for = 'featureSortByNumThemes';
  featureSortByNumThemesInputLabel.innerHTML = 'numThemes';
  featureSortByNumThemesInputDiv.appendChild(featureSortByNumThemesInputLabel);

  featureSelectionHeadingRow.appendChild(featureSelectionHeading);
  featureSelectionHeadingRow.appendChild(featureSortByNameInputDiv);
  featureSelectionHeadingRow.appendChild(featureSortByNumThemesInputDiv);
  selectionMenuDiv.appendChild(featureSelectionHeadingRow);
}

function buildTagSelectionDiv(selectedTags, availableTags, tagSortBy) {
  let selectionMenuDiv = document.getElementById('selection-menu');
  buildTagSelectionHeadingRow(selectionMenuDiv, tagSortBy);

  let tagSelectionRow = document.createElement('div');
  tagSelectionRow.style.display = 'flex';
  tagSelectionRow.style.flexWrap = 'wrap';
  tagSelectionRow.style.justifyContent = 'space-around';

  selectionMenuDiv.appendChild(tagSelectionRow);

  availableTags
    .filter((x) => selectedTags.includes(x.tag))
    .forEach((y) => { buildTagSelectionInput(y, true, tagSelectionRow); });

  availableTags
    .filter((x) => !selectedTags.includes(x.tag))
    .forEach((y) => { buildTagSelectionInput(y, false, tagSelectionRow); });
}

function buildFeatureSelectionDiv(selectedFeatures, availableFeatures, featureSortBy) {
  let selectionMenuDiv = document.getElementById('selection-menu');
  buildFeatureSelectionHeadingRow(selectionMenuDiv, featureSortBy);

  let featureSelectionRow = document.createElement('div');
  featureSelectionRow.style.display = 'flex';
  featureSelectionRow.style.flexWrap = 'wrap';
  featureSelectionRow.style.justifyContent = 'space-around';

  selectionMenuDiv.appendChild(featureSelectionRow);

  availableFeatures
    .filter((x) => selectedFeatures.includes(x.feature))
    .forEach((y) => { buildFeatureSelectionInput(y, true, featureSelectionRow); });

  availableFeatures
    .filter((x) => !selectedFeatures.includes(x.feature))
    .forEach((y) => { buildFeatureSelectionInput(y, false, featureSelectionRow); });
}

function buildSelectionMenu(sorted_themes, sortedBy, selectedTags, selectedFeatures) {
  let tagSortBy = getTagSortBy();
  let featureSortBy = getFeatureSortBy();
  let availableTags = getAvailableTags(sorted_themes, tagSortBy);
  let availableFeatures = getAvailableFeatures(sorted_themes, featureSortBy);
  buildSortByDiv(sortedBy);
  buildTagSelectionDiv(selectedTags, availableTags, tagSortBy);
  buildFeatureSelectionDiv(selectedFeatures, availableFeatures, featureSortBy);
}
