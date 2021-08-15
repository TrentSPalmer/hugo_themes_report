// called from buildSelectionMenu.js
function getAvailableFeatures(sorted_themes, featureSortBy) {
  let result = [];
  sorted_themes.forEach((x) => {
    x.features.forEach((feature) => {
      if (result.length === 0) {
        result.push({ feature: feature, num_themes: 1 });
      } else {
        let features_in_result = result.map((y) => y.feature);
        if (features_in_result.includes(feature)) {
          result.forEach((w) => {
            if (w.feature === feature) {
              w.num_themes += 1;
            }
          });
        } else {
          result.push({ feature: feature, num_themes: 1 });
        }
      }
    });
  });
  if (featureSortBy === "numThemes") {
    return result
      .sort((a, b) => a.feature.localeCompare(b.feature))
      .sort((a, b) => b.num_themes - a.num_themes);
  } else {
    return result.sort((a, b) => a.feature.localeCompare(b.feature));
  }
}

// called from buildSelectionMenu.js
function getAvailableTags(sorted_themes, tagSortBy) {
  let result = [];
  sorted_themes.forEach((x) => {
    x.tags.forEach((tag) => {
      if (result.length === 0) {
        result.push({ tag: tag, num_themes: 1 });
      } else {
        let tags_in_result = result.map((y) => y.tag);
        if (tags_in_result.includes(tag)) {
          result.forEach((w) => {
            if (w.tag === tag) {
              w.num_themes += 1;
            }
          });
        } else {
          result.push({ tag: tag, num_themes: 1 });
        }
      }
    });
  });
  if (tagSortBy === "numThemes") {
    return result
      .sort((a, b) => a.tag.localeCompare(b.tag))
      .sort((a, b) => b.num_themes - a.num_themes);
  } else {
    return result.sort((a, b) => a.tag.localeCompare(b.tag));
  }
}
