function getAvailableMinVersions() {
  let availableMinVersions = [];
  themes.forEach((x) => {
    if (x.min_ver !== "") {
      if (!availableMinVersions.includes(x.min_ver)) {
        availableMinVersions.push(x.min_ver);
      }
    }
  });
  // semVerCompare comes from getSortedThemes.js
  return availableMinVersions
    .sort((a, b) => semVerCompare(a, b))
    .map((x) => x.toLowerCase().replace(/[\s*]/g, "-"));
}

function buildMinVerSelectionHeadingRow(eParent, dState) {
  let minVerSelectionHeadingRow = document.createElement("div");
  minVerSelectionHeadingRow.id = "minVerSelectionHeadingRow";
  minVerSelectionHeadingRow.style.maxWidth = "100%";
  minVerSelectionHeadingRow.style.display = dState.minVerSelectionHeadingRow;
  // minVerSelectionHeadingRow.style.display = "flex";
  minVerSelectionHeadingRow.style.alignItems = "center";

  let minVerSelectionHeading = document.createElement("h2");
  minVerSelectionHeading.innerHTML = "MinVersion";
  minVerSelectionHeadingRow.appendChild(minVerSelectionHeading);
  eParent.appendChild(minVerSelectionHeadingRow);
}

function buildMinVerSelectionDiv(selectedMinVer, dState, eParent) {
  buildMinVerSelectionHeadingRow(eParent, dState);

  let minVerSelectionRow = document.createElement("div");
  minVerSelectionRow.id = "minVerSelectionRow";
  minVerSelectionRow.style.display = dState.minVerSelectionRow;
  // minVerSelectionRow.style.display = "flex";
  minVerSelectionRow.style.flexWrap = "wrap";
  minVerSelectionRow.style.justifyContent = "space-around";
  eParent.appendChild(minVerSelectionRow);

  let availableMinVersions = getAvailableMinVersions();
  availableMinVersions.push("none");
  let selMinVer = selectedMinVer.length === 0 ? "none" : selectedMinVer[0];

  availableMinVersions.forEach((x) => {
    let inputID = `${x}-select-minver-radio-button-input`;
    let rButton = buildRadioButton(
      inputID,
      "minVerRadioButtonSelectionInput",
      x,
      selMinVer,
      x,
      x
    );
    minVerSelectionRow.appendChild(rButton);
    let filterByMinVerInput = document.getElementById(inputID);
    rButton.onclick = function () {
      if (!filterByMinVerInput.checked) {
        filterByMinVerInput.checked = true;
        buildResults();
      }
    };
  });
}
