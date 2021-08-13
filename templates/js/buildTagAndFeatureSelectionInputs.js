function buildTagSelectionInput(tag, selected, tagSelectionRow) {
  let tagSelectionInputButton = document.createElement("button");
  tagSelectionInputButton.style.width = "15rem";
  tagSelectionInputButton.style.maxWidth = "50%";
  tagSelectionInputButton.style.margin = ".5rem";
  tagSelectionInputButton.style.display = "flex";
  tagSelectionInputButton.style.alignItems = "center";

  let tagSelectionInput = document.createElement("input");
  tagSelectionInput.style.marginRight = "1rem";
  tagSelectionInput.type = "checkbox";
  tagSelectionInput.id = tag.tag + "-selection-input";
  tagSelectionInput.name = tag.tag + "-selection-input";
  tagSelectionInput.value = tag.tag;
  tagSelectionInput.checked = selected ? true : false;
  tagSelectionInput.classList.add("tagSelectionInput");
  tagSelectionInput.onclick = function () {
    buildResults();
  };
  tagSelectionInputButton.appendChild(tagSelectionInput);

  let tagSelectionInputLabel = document.createElement("label");
  tagSelectionInputLabel.style.textAlign = "left";
  tagSelectionInputLabel.for = tag.tag + "-selection-input";
  tagSelectionInputLabel.innerHTML = tag.tag + " (" + tag.num_themes + ")";
  tagSelectionInputButton.appendChild(tagSelectionInputLabel);
  tagSelectionInputButton.onclick = function () {
    tagSelectionInput.checked = !tagSelectionInput.checked;
    buildResults();
  };

  tagSelectionRow.appendChild(tagSelectionInputButton);
}

function buildFeatureSelectionInput(feature, selected, featureSelectionRow) {
  let featureSelectionInputButton = document.createElement("button");
  featureSelectionInputButton.style.width = "30rem";
  featureSelectionInputButton.style.maxWidth = "50%";
  featureSelectionInputButton.style.margin = ".5rem";
  featureSelectionInputButton.style.display = "flex";
  featureSelectionInputButton.style.alignItems = "center";

  let featureSelectionInput = document.createElement("input");
  featureSelectionInput.style.marginRight = "1rem";
  featureSelectionInput.type = "checkbox";
  featureSelectionInput.id = feature.feature + "-selection-input";
  featureSelectionInput.name = feature.feature + "-selection-input";
  featureSelectionInput.value = feature.feature;
  featureSelectionInput.checked = selected ? true : false;
  featureSelectionInput.classList.add("featureSelectionInput");
  featureSelectionInput.onclick = function () {
    buildResults();
  };
  featureSelectionInputButton.appendChild(featureSelectionInput);

  let featureSelectionInputLabel = document.createElement("label");
  featureSelectionInputLabel.style.textAlign = "left";
  featureSelectionInputLabel.for = feature.feature + "-selection-input";
  featureSelectionInputLabel.innerHTML =
    feature.feature + " (" + feature.num_themes + ")";
  featureSelectionInputButton.appendChild(featureSelectionInputLabel);
  featureSelectionInputButton.onclick = function () {
    featureSelectionInput.checked = !featureSelectionInput.checked;
    buildResults();
  };

  featureSelectionRow.appendChild(featureSelectionInputButton);
}
