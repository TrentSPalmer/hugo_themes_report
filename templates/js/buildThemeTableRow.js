function addThemeTableRow(theme) {
  let resultsTable = document.getElementById("resultsTable");
  let resultsTableRow = document.createElement("tr");

  let themeTD = document.createElement("td");
  themeTD.innerHTML =
    '<a href="' + theme.url + '" target="_blank">' + theme.cname + "</a>";
  themeTD.style.minWidth = `${theme.cname.length / 6}rem`;
  resultsTableRow.appendChild(themeTD);

  let dateTD = document.createElement("td");
  dateTD.innerHTML = theme.date;
  dateTD.style.minWidth = "5rem";
  resultsTableRow.appendChild(dateTD);

  let starsTD = document.createElement("td");
  starsTD.innerHTML = theme.num_stars;
  resultsTableRow.appendChild(starsTD);

  let commitTD = document.createElement("td");
  commitTD.innerHTML = theme.commit;
  resultsTableRow.appendChild(commitTD);

  let minVerTD = document.createElement("td");
  minVerTD.innerHTML = theme.min_ver;
  resultsTableRow.appendChild(minVerTD);

  let licenseTD = document.createElement("td");
  licenseTD.innerHTML = theme.license;
  licenseTD.style.minWidth = `${theme.license.length / 7}rem`;
  resultsTableRow.appendChild(licenseTD);

  let descTD = document.createElement("td");
  descTD.innerHTML = theme.desc;
  descTD.style.minWidth = `${theme.desc.length / 7}rem`;
  resultsTableRow.appendChild(descTD);

  let tagsTD = document.createElement("td");
  let tL = theme.tags.length - 1;
  tL += theme.tags.map((x) => x.length).reduce((a, b) => a + b, 0);
  tagsTD.innerHTML = theme.tags;
  tagsTD.style.minWidth = `${tL / 7}rem`;
  resultsTableRow.appendChild(tagsTD);

  let featuresTD = document.createElement("td");
  let fL = theme.features.length - 1;
  fL += theme.features.map((x) => x.length).reduce((a, b) => a + b, 0);
  featuresTD.innerHTML = theme.features;
  featuresTD.style.minWidth = `${fL / 7}rem`;
  resultsTableRow.appendChild(featuresTD);

  resultsTable.appendChild(resultsTableRow);
}
