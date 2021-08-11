function buildTagSelectionInput(tag, selected, tagSelectionRow) {
  let tagSelectionInputDiv = document.createElement('div');
  tagSelectionInputDiv.style.width = '15rem';
  tagSelectionInputDiv.style.maxWidth = '50%';
  tagSelectionInputDiv.style.marginTop = '.5rem';
  tagSelectionInputDiv.style.marginBottom = '.5rem';

  let tagSelectionInput = document.createElement('input');
  tagSelectionInput.type = "checkbox";
  tagSelectionInput.id = tag.tag + "-selection-input";
  tagSelectionInput.name = tag.tag + "-selection-input";
  tagSelectionInput.value = tag.tag;
  tagSelectionInput.checked = (selected) ? true : false;
  tagSelectionInput.classList.add('tagSelectionInput');
  tagSelectionInput.onclick = function() { buildResults(); };
  tagSelectionInputDiv.appendChild(tagSelectionInput);

  let tagSelectionInputLabel = document.createElement('label');
  tagSelectionInputLabel.for = tag.tag + "-selection-input";
  tagSelectionInputLabel.innerHTML = tag.tag + ' (' + tag.num_themes + ')';
  tagSelectionInputDiv.appendChild(tagSelectionInputLabel);

  tagSelectionRow.appendChild(tagSelectionInputDiv);
}

function buildTagSelectionDiv(selectedTags, availableTags) {
  let selectionMenuDiv = document.getElementById('selection-menu');
  let tagSelectionHeading = document.createElement('h2');
  tagSelectionHeading.innerHTML = "Select Tags";
  selectionMenuDiv.appendChild(tagSelectionHeading);

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

function buildFeatureSelectionInput(feature, selected, featureSelectionRow) {
  let featureSelectionInputDiv = document.createElement('div');
  featureSelectionInputDiv.style.width = '30rem';
  featureSelectionInputDiv.style.maxWidth = '50%';
  featureSelectionInputDiv.style.marginTop = '.5rem';
  featureSelectionInputDiv.style.marginBottom = '.5rem';

  let featureSelectionInput = document.createElement('input');
  featureSelectionInput.type = "checkbox";
  featureSelectionInput.id = feature.feature + "-selection-input";
  featureSelectionInput.name = feature.feature + "-selection-input";
  featureSelectionInput.value = feature.feature;
  featureSelectionInput.checked = (selected) ? true : false;
  featureSelectionInput.classList.add('featureSelectionInput');
  featureSelectionInput.onclick = function() { buildResults(); };
  featureSelectionInputDiv.appendChild(featureSelectionInput);

  let featureSelectionInputLabel = document.createElement('label');
  featureSelectionInputLabel.for =  feature.feature + "-selection-input";
  featureSelectionInputLabel.innerHTML = feature.feature + ' (' + feature.num_themes + ')';
  featureSelectionInputDiv.appendChild(featureSelectionInputLabel);

  featureSelectionRow.appendChild(featureSelectionInputDiv);
}

function buildFeatureSelectionDiv(selectedFeatures, availableFeatures) {
  let selectionMenuDiv = document.getElementById('selection-menu');
  let featureSelectionHeading = document.createElement('h2');
  featureSelectionHeading.innerHTML = "Select Features";
  selectionMenuDiv.appendChild(featureSelectionHeading);

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
  let availableTags = getAvailableTags(sorted_themes);
  let availableFeatures = getAvailableFeatures(sorted_themes);
  buildSortByDiv(sortedBy);
  buildTagSelectionDiv(selectedTags, availableTags);
  buildFeatureSelectionDiv(selectedFeatures, availableFeatures);
}
