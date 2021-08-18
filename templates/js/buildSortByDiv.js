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
    "sortByStars",
    "sortBy",
    "stars",
    sortBy[0],
    "stars",
    "Stars"
  );

  // from buildButton.js
  let sortByLastCommitButton = buildRadioButton(
    "sortByDate",
    "sortBy",
    "date",
    sortBy[0],
    "date",
    "Latest Commit Date"
  );

  // from buildButton.js
  let sortByMinVerButton = buildRadioButton(
    "sortByMinVer",
    "sortBy",
    "minVer",
    sortBy[0],
    "minVer",
    "Min Hugo Version"
  );

  // from buildButton.js
  let sortByLicenseButton = buildRadioButton(
    "sortByLicense",
    "sortBy",
    "license",
    sortBy[0],
    "license",
    "License"
  );

  // from buildButton.js
  let sortByNameButton = buildRadioButton(
    "sortByName",
    "sortBy",
    "name",
    sortBy[0],
    "name",
    "Name"
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
