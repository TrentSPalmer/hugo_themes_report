function buildSortByDiv(sortedBy) {
  let menuDiv = document.getElementById('selection-menu');
  menuDiv.innerHTML = '';
  menuDiv.style.maxWidth = '100%';

  let sortByRow = document.createElement('div');
  sortByRow.id = 'sortByRow';
  sortByRow.style.width = '500px';
  sortByRow.style.maxWidth = '100%';
  sortByRow.style.display = 'flex';
  sortByRow.style.justifyContent = 'space-around';
  sortByRow.style.margin = '1rem auto 1rem auto';

  let sortByPrompt = document.createElement('div');
  sortByPrompt.innerHTML = "Sort By:";
  sortByRow.appendChild(sortByPrompt);

  let sortByStarsDiv = document.createElement('div');
  let sortByStarsInput = document.createElement('input');
  sortByStarsInput.type = 'radio';
  sortByStarsInput.id = 'sortByStars';
  sortByStarsInput.name = 'sortBy';
  sortByStarsInput.value = 'stars';
  sortByStarsInput.checked = sortedBy === 'stars' ? true : false;
  sortByStarsInput.onclick = function() { buildResults(); };
  sortByStarsDiv.appendChild(sortByStarsInput);

  let sortByStarsLabel = document.createElement('label');
  sortByStarsLabel.for = 'stars';
  sortByStarsLabel.innerHTML = 'Stars';
  sortByStarsDiv.appendChild(sortByStarsLabel);

  let sortByLastCommitDiv = document.createElement('div');
  let sortByLastCommitInput = document.createElement('input');
  sortByLastCommitInput.type = 'radio';
  sortByLastCommitInput.id = 'sortByDate';
  sortByLastCommitInput.name = 'sortBy';
  sortByLastCommitInput.value = 'date';
  sortByLastCommitInput.checked = sortedBy === 'date' ? true : false;
  sortByLastCommitInput.onclick = function() { buildResults(); };
  sortByLastCommitDiv.appendChild(sortByLastCommitInput);

  let sortByLastCommitLabel = document.createElement('label');
  sortByLastCommitLabel.for = 'date';
  sortByLastCommitLabel.innerHTML = 'Latest Commit Date';
  sortByLastCommitDiv.appendChild(sortByLastCommitLabel);


  sortByRow.appendChild(sortByStarsDiv);
  sortByRow.appendChild(sortByLastCommitDiv);

  menuDiv.appendChild(sortByRow);
}
