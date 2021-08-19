function buildDescription(
  selectedColumns,
  sortBy,
  selectedMinVer,
  selectedLicenses,
  selectedTags,
  selectedFeatures
) {
  let d = document.getElementById("description");
  d.style.fontSize = ".9rem";
  d.style.color = "gray";
  d.style.fontStyle = "italic";
  d.style.textAlign = "left";
  let sCols = selectedColumns.map((x) => {
    if (x === "cname") {
      return "theme";
    } else if (x === "num_stars") {
      return "stars";
    } else if (x === "min_ver") {
      return "minVer";
    } else {
      return x;
    }
  });
  let showingColumns = `<span style="color: blue;font-weight: bold">ShowingColumns:</span> ${sCols}; `;
  let sortedBy = `<span style="color: blue;font-weight: bold">SortedBy:</span> ${sortBy}; `;
  let sMinVer = `<span style="color: green;font-weight: bold">MinHugoVersion</span>=${
    selectedMinVer.length === 0 ? "none" : selectedMinVer
  }; `;
  let sLicences = `<span style="color: green;font-weight: bold">Licenses</span>=${
    selectedLicenses.length === 0 ? "none" : selectedLicenses
  }; `;
  let sTags = `<span style="color: green;font-weight: bold">Tags</span>=${
    selectedTags.length === 0 ? "none" : selectedTags
  }; `;
  let sFeatures = `<span style="color: green;font-weight: bold">Features</span>=${
    selectedFeatures.length === 0 ? "none" : selectedFeatures
  }`;
  let innerHTML =
    showingColumns +
    sortedBy +
    " <span style='color: blue;font-weight: bold'>FilteredBy:</span> " +
    sMinVer +
    sLicences +
    sTags +
    sFeatures;
  d.innerHTML = innerHTML.replace(/[,]/g, ", ");
}
