function addThemeTableRow(theme) {
  let resultsTable = document.getElementById('resultsTable');
  let resultsTableRow = document.createElement("tr");

  let themeTD = document.createElement("td");
  themeTD.innerHTML = '<a href="' + theme.url + '" target="_blank">' + theme.short_name + '</a>';
  themeTD.style.whiteSpace = 'nowrap';
  themeTD.style.overFlow = 'hidden';
  themeTD.style.width = '20%';
  resultsTableRow.appendChild(themeTD);

  let dateTD = document.createElement("td");
  dateTD.innerHTML = theme.date;
  dateTD.style.textAlign = 'center';
  dateTD.style.minWidth = '8rem';
  resultsTableRow.appendChild(dateTD);

  let starsTD = document.createElement("td");
  starsTD.innerHTML = theme.num_stars;
  resultsTableRow.appendChild(starsTD);

  let commitTD = document.createElement("td");
  commitTD.innerHTML = theme.commit;
  commitTD.style.minWidth = '7rem';
  resultsTableRow.appendChild(commitTD);

  resultsTable.appendChild(resultsTableRow);
};
