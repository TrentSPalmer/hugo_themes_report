// called from buildSelectionMenu.js
function buildSortByDiv(sortBy, sortByRowDisplay) {
  let menuDiv = document.getElementById("selection-menu");
  menuDiv.innerHTML = "";
  menuDiv.style.maxWidth = "100%";

  let sortByRow = document.createElement("div");
  sortByRow.id = "sortByRow";
  // sortByRow.style.width = "500px";
  sortByRow.style.maxWidth = "100%";
  sortByRow.style.display = sortByRowDisplay;
  sortByRow.style.flexWrap = "wrap";
  sortByRow.style.justifyContent = "space-around";
  sortByRow.style.margin = "1rem auto 1rem auto";

  let sortByPrompt = document.createElement("div");
  sortByPrompt.style.display = "flex";
  sortByPrompt.style.alignItems = "center";
  sortByPrompt.innerHTML = "Sort By:";
  sortByRow.appendChild(sortByPrompt);

  // from buildButton.js
  let sortByStarsButton = buildRadioButton(
    (inputID = "sortByStars"),
    (inputName = "sortBy"),
    (inputValue = "stars"),
    (sortedBy = sortBy[0]),
    (sortedBySelector = "stars"),
    (labelText = "Stars")
  );

  // from buildButton.js
  let sortByLastCommitButton = buildRadioButton(
    (inputID = "sortByDate"),
    (inputName = "sortBy"),
    (inputValue = "date"),
    (sortedBy = sortBy[0]),
    (sortedBySelector = "date"),
    (labelText = "Latest Commit Date")
  );

  // from buildButton.js
  let sortByMinVerButton = buildRadioButton(
    (inputID = "sortByMinVer"),
    (inputName = "sortBy"),
    (inputValue = "minVer"),
    (sortedBy = sortBy[0]),
    (sortedBySelector = "minVer"),
    (labelText = "Min Hugo Version")
  );

  // from buildButton.js
  let sortByLicenseButton = buildRadioButton(
    (inputID = "sortByLicense"),
    (inputName = "sortBy"),
    (inputValue = "license"),
    (sortedBy = sortBy[0]),
    (sortedBySelector = "license"),
    (labelText = "License")
  );

  // from buildButton.js
  let sortByNameButton = buildRadioButton(
    (inputID = "sortByName"),
    (inputName = "sortBy"),
    (inputValue = "name"),
    (sortedBy = sortBy[0]),
    (sortedBySelector = "name"),
    (labelText = "Name")
  );

  sortBy.forEach((x) => {
    if (x === "date") {
      sortByRow.appendChild(sortByLastCommitButton);
    } else if (x === "name") {
      sortByRow.appendChild(sortByNameButton);
    } else if (x === "minVer") {
      sortByRow.appendChild(sortByMinVerButton);
    } else if (x === "license") {
      sortByRow.appendChild(sortByLicenseButton);
    } else if (x === "stars") {
      sortByRow.appendChild(sortByStarsButton);
    }
  });

  menuDiv.appendChild(sortByRow);

  let sortByMinVerInput = document.getElementById("sortByMinVer");
  sortByMinVerButton.onclick = function () {
    if (!sortByMinVerInput.checked) {
      sortByMinVerInput.checked = true;
      buildResults();
    }
  };

  let sortByLicenseInput = document.getElementById("sortByLicense");
  sortByLicenseButton.onclick = function () {
    if (!sortByLicenseInput.checked) {
      sortByLicenseInput.checked = true;
      buildResults();
    }
  };

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

  let sortByNameInput = document.getElementById("sortByName");
  sortByNameButton.onclick = function () {
    if (!sortByNameInput.checked) {
      sortByNameInput.checked = true;
      buildResults();
    }
  };
}
