function getAvailableFeatures(sorted_themes) {
  let result = [];
  sorted_themes.forEach(x => {
    x.features.forEach(feature => {
      if (result.length === 0) {
        result.push({'feature': feature, 'num_themes': 1});
      } else {
        let features_in_result = result.map(y => y.feature);
        if (features_in_result.includes(feature)) {
          result.forEach(w => {
            if (w.feature === feature) {
              w.num_themes += 1;
            }
          });
        } else {
          result.push({'feature': feature, 'num_themes': 1});
        }
      }
    });
  });
  // return result.sort((a, b) => a.feature.localeCompare(b.feature));
  return result.sort((a, b) => b.num_themes - a.num_themes);
}

function getAvailableTags(sorted_themes) {
  let result = [];
  sorted_themes.forEach(x => {
    x.tags.forEach(tag => {
      if (result.length === 0) {
        result.push({'tag': tag, 'num_themes': 1});
      } else {
        let tags_in_result = result.map(y => y.tag);
        if (tags_in_result.includes(tag)) {
          result.forEach(w => {
            if (w.tag === tag) {
              w.num_themes += 1;
            }
          });
        } else {
          result.push({'tag': tag, 'num_themes': 1});
        }
      }
    });
  });
  return result.sort((a, b) => b.num_themes - a.num_themes);
}


