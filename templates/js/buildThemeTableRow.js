function addThemeTableRow(theme, selectedColumns, selectedTags) {
  let resultsTable = document.getElementById("resultsTable");
  let resultsTableRow = document.createElement("tr");

  if (selectedColumns.includes("cname")) {
    let themeTD = document.createElement("td");
    themeTD.innerHTML =
      '<a href="' + theme.url + '" target="_blank">' + theme.cname + "</a>";
    themeTD.style.minWidth = `${theme.cname.length / 6}rem`;
    resultsTableRow.appendChild(themeTD);
  }

  if (selectedColumns.includes("date")) {
    let dateTD = document.createElement("td");
    dateTD.innerHTML = theme.date;
    dateTD.style.minWidth = "5rem";
    resultsTableRow.appendChild(dateTD);
  }

  if (selectedColumns.includes("num_stars")) {
    let starsTD = document.createElement("td");
    starsTD.innerHTML = theme.num_stars;
    resultsTableRow.appendChild(starsTD);
  }

  if (selectedColumns.includes("commit")) {
    let commitTD = document.createElement("td");
    commitTD.innerHTML = theme.commit;
    resultsTableRow.appendChild(commitTD);
  }

  if (selectedColumns.includes("min_ver")) {
    let minVerTD = document.createElement("td");
    minVerTD.innerHTML = theme.min_ver;
    resultsTableRow.appendChild(minVerTD);
  }

  if (selectedColumns.includes("license")) {
    let licenseTD = document.createElement("td");
    licenseTD.innerHTML = theme.license;
    licenseTD.style.minWidth = `${theme.license.length / 7}rem`;
    resultsTableRow.appendChild(licenseTD);
  }

  if (selectedColumns.includes("desc")) {
    let descTD = document.createElement("td");
    descTD.innerHTML = theme.desc;
    descTD.style.minWidth = `${theme.desc.length / 7}rem`;
    resultsTableRow.appendChild(descTD);
  }

  if (selectedColumns.includes("tags")) {
    let tagsTD = document.createElement("td");
    let tL = theme.tags.length - 1;
    tL += theme.tags.map((x) => x.length).reduce((a, b) => a + b, 0);
    let sTags = theme.tags.filter((x) => selectedTags.includes(x));
    let nsTags = theme.tags.filter((x) => !selectedTags.includes(x));
    if (sTags.length > 0 && nsTags.length > 0) {
      tagsTD.innerHTML = `<span style="color: green">${sTags}</span>,${nsTags}`;
    } else {
      tagsTD.innerHTML = `<span style="color: green">${sTags}</span>${nsTags}`;
    }
    tagsTD.style.minWidth = `${tL / 7}rem`;
    resultsTableRow.appendChild(tagsTD);
  }

  if (selectedColumns.includes("features")) {
    let featuresTD = document.createElement("td");
    let fL = theme.features.length - 1;
    fL += theme.features.map((x) => x.length).reduce((a, b) => a + b, 0);
    featuresTD.innerHTML = theme.features;
    featuresTD.style.minWidth = `${fL / 7}rem`;
    resultsTableRow.appendChild(featuresTD);
  }

  resultsTable.appendChild(resultsTableRow);
}
