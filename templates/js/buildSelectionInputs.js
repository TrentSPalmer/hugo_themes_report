// called from buildTagAndFeatureSelectionDivs.js
function buildInput(item, selected, inpParent) {
  let inputSelectionButton = document.createElement("button");
  inputSelectionButton.style.maxWidth = "calc(50% - 2rem)";
  inputSelectionButton.style.margin = ".5rem";
  inputSelectionButton.style.display = "flex";
  inputSelectionButton.style.alignItems = "center";

  let selectionInput = document.createElement("input");
  selectionInput.style.marginRight = "1rem";
  selectionInput.type = "checkbox";
  selectionInput.checked = selected ? true : false;
  selectionInput.onclick = function () {
    buildResults();
  };
  inputSelectionButton.appendChild(selectionInput);

  let selectionInputLabel = document.createElement("label");
  selectionInputLabel.style.textAlign = "left";
  inputSelectionButton.appendChild(selectionInputLabel);
  inputSelectionButton.onclick = function () {
    selectionInput.checked = !selectionInput.checked;
    buildResults();
  };

  if ("feature" in item) {
    selectionInput.value = item.feature;
    inputSelectionButton.style.width = "15rem";
    selectionInputLabel.innerHTML = `${item.feature} (${item.num_themes})`;
    selectionInput.classList.add("featureSelectionInput");
  } else if ("tag" in item) {
    selectionInput.value = item.tag;
    inputSelectionButton.style.width = "12rem";
    selectionInputLabel.innerHTML = `${item.tag} (${item.num_themes})`;
    selectionInput.classList.add("tagSelectionInput");
  } else if ("headingName" in item) {
    selectionInput.value = `${item.headingName}-column`;
    selectionInputLabel.innerHTML = item.headingText;
    selectionInput.classList.add("columnSelectionInput");
  }

  selectionInput.id = `${selectionInput.value}-selection-input`;
  selectionInput.name = `${selectionInput.id}`;
  selectionInputLabel.for = `${selectionInput.id}`;

  inpParent.appendChild(inputSelectionButton);
}
