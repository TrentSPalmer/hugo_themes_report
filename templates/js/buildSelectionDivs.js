// called from buildSelectionMenu.js
function buildSelectionDiv(
  selectedItems,
  availableItems,
  sortBy,
  dStateSelectionRow,
  dStateSelectionHeadingRow,
  eParent,
  menuSection
) {
  // from buildSelectionHeadingRows.js
  buildSelectionHeadingRow(
    eParent,
    sortBy,
    dStateSelectionHeadingRow,
    menuSection
  );

  let selectionRow = document.createElement("div");
  selectionRow.id = `${menuSection}SelectionRow`;
  selectionRow.style.display = dStateSelectionRow;
  selectionRow.style.flexWrap = "wrap";
  selectionRow.style.justifyContent = "space-around";

  eParent.appendChild(selectionRow);

  availableItems
    .filter((x) => selectedItems.includes(x[menuSection]))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, true, selectionRow);
    });

  availableItems
    .filter((x) => !selectedItems.includes(x[menuSection]))
    .forEach((y) => {
      // from buildSelectionInputs.js
      buildInput(y, false, selectionRow);
    });
}
