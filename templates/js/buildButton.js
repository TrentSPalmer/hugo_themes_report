function buildRadioButton(
  inputID,
  inputName,
  inputValue,
  sortedBy,
  sortedBySelector,
  labelText
) {
  let result = document.createElement("button");

  result.style.display = "flex";
  result.style.alignItems = "center";
  result.style.height = "2rem";
  result.style.margin = ".5rem";

  let inputAttsA = `id=${inputID} type="radio" name=${inputName} value=${inputValue}`;
  let inputAttsB = `onclick="buildResults()" style="margin:0 1rem 0 0" class=${inputName}`;
  let inputAttsC = sortedBy === sortedBySelector ? " checked" : "";
  let resultButtonInput = `<input ${inputAttsA} ${inputAttsB} ${inputAttsC}/>`;

  let resultButtonLabel = `<label for=${inputID}>${labelText}</label>`;

  result.innerHTML = `${resultButtonInput}${resultButtonLabel}`;
  return result;
}
