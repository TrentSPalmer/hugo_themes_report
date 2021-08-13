function buildSortByDiv(sortedBy) {
  let menuDiv = document.getElementById("selection-menu");
  menuDiv.innerHTML = "";
  menuDiv.style.maxWidth = "100%";

  let sortByRow = document.createElement("div");
  sortByRow.id = "sortByRow";
  sortByRow.style.width = "500px";
  sortByRow.style.maxWidth = "100%";
  sortByRow.style.display = "flex";
  sortByRow.style.justifyContent = "space-around";
  sortByRow.style.margin = "1rem auto 1rem auto";

  let sortByPrompt = document.createElement("div");
  sortByPrompt.style.display = "flex";
  sortByPrompt.style.alignItems = "center";
  sortByPrompt.innerHTML = "Sort By:";
  sortByRow.appendChild(sortByPrompt);

  let sortByStarsButton = buildRadioButton(
    (inputID = "sortByStars"),
    (inputName = "sortBy"),
    (inputValue = "stars"),
    (sortedBy = sortedBy),
    (sortedBySelector = "stars"),
    (labelText = "Stars")
  );

  let sortByLastCommitButton = buildRadioButton(
    (inputID = "sortByDate"),
    (inputName = "sortBy"),
    (inputValue = "date"),
    (sortedBy = sortedBy),
    (sortedBySelector = "date"),
    (labelText = "Latest Commit Date")
  );

  sortByRow.appendChild(sortByStarsButton);
  sortByRow.appendChild(sortByLastCommitButton);
  menuDiv.appendChild(sortByRow);

  let sortByStarsInput = document.getElementById("sortByStars");
  sortByStarsButton.onclick = function () {
    if (!sortByStarsInput.checked) {
      sortByStarsInput.checked = true;
      buildResults();
    }
  };
  let sortByLastCommitInput = document.getElementById("sortByDate");
  sortByLastCommitButton.onclick = function () {
    if (!sortByLastCommitInput.checked) {
      sortByLastCommitInput.checked = true;
      buildResults();
    }
  };
}
