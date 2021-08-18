// called from buildTagAndFeatureSelectionDivs.js
function buildSelectionHeadingRow(
  eParent,
  sortBy,
  dStateSelectionHeadingRow,
  menuSection
) {
  let selectionHeadingRow = document.createElement("div");
  selectionHeadingRow.id = `${menuSection}SelectionHeadingRow`;
  selectionHeadingRow.style.maxWidth = "100%";
  selectionHeadingRow.style.display = dStateSelectionHeadingRow;
  selectionHeadingRow.style.justifyContent = "space-around";
  selectionHeadingRow.style.alignItems = "center";

  let selectionHeading = document.createElement("h2");
  selectionHeading.innerHTML = `Select ${menuSection}s`;

  let sortByNameInputButton = buildRadioButton(
    `${menuSection}SortByName`,
    `${menuSection}SortBy`,
    `${menuSection}SortByName`,
    sortBy,
    "name",
    "Name"
  );

  let sortByNumThemesInputButton = buildRadioButton(
    `${menuSection}SortByNumThemes`,
    `${menuSection}SortBy`,
    `${menuSection}SortByNumThemes`,
    sortBy,
    "numThemes",
    "nThemes"
  );

  selectionHeadingRow.appendChild(selectionHeading);
  selectionHeadingRow.appendChild(sortByNameInputButton);
  selectionHeadingRow.appendChild(sortByNumThemesInputButton);
  eParent.appendChild(selectionHeadingRow);

  let sortByNameInput = document.getElementById(`${menuSection}SortByName`);
  sortByNameInputButton.onclick = function () {
    if (!sortByNameInput.checked) {
      sortByNameInput.checked = true;
      buildResults();
    }
  };

  let sortByNumThemesInput = document.getElementById(
    `${menuSection}SortByNumThemes`
  );
  sortByNumThemesInputButton.onclick = function () {
    if (!sortByNumThemesInput.checked) {
      sortByNumThemesInput.checked = true;
      buildResults();
    }
  };
}
