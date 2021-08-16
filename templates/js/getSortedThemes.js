function dateCompare(x, y) {
  let xRay = x.split("-").map((j) => parseInt(j));
  let yRay = y.split("-").map((k) => parseInt(k));
  return xRay[0] > yRay[0]
    ? 1
    : xRay[0] < yRay[0]
    ? -1
    : xRay[1] > yRay[1]
    ? 1
    : xRay[1] < yRay[1]
    ? -1
    : xRay[2] > yRay[2]
    ? 1
    : xRay[2] < yRay[2]
    ? -1
    : 0;
}

function semVerCompare(y, x) {
  let xRay = x.split(".").map((j) => parseInt(j));
  let yRay = y.split(".").map((k) => parseInt(k));
  [xRay, yRay].forEach((i) => {
    if (i.length < 1) {
      i[0] = 0;
      i[1] = 0;
      i[2] = 0;
    } else if (i.length < 2) {
      i[1] = 0;
      i[2] = 0;
    } else if (i.length < 3) {
      i[2] = 0;
    }
  });
  return xRay[0] > yRay[0]
    ? 1
    : xRay[0] < yRay[0]
    ? -1
    : xRay[1] > yRay[1]
    ? 1
    : xRay[1] < yRay[1]
    ? -1
    : xRay[2] > yRay[2]
    ? 1
    : xRay[2] < yRay[2]
    ? -1
    : 0;
}

function compareTheme(x, y, sortedBy) {
  if (sortedBy[0] === "date") {
    let dComp = dateCompare(y.date, x.date);
    return dComp === 1
      ? 1
      : dComp === -1
      ? -1
      : sortedBy.length < 2
      ? -1
      : compareTheme(x, y, sortedBy.slice(1));
  } else if (sortedBy[0] === "stars") {
    return y.num_stars > x.num_stars
      ? 1
      : y.num_stars < x.num_stars
      ? -1
      : sortedBy.length < 2
      ? -1
      : compareTheme(x, y, sortedBy.slice(1));
  } else if (sortedBy[0] === "name") {
    return x.cname.localeCompare(y.cname) === 1
      ? 1
      : x.cname.localeCompare(y.cname) === -1
      ? -1
      : sortedBy.length < 2
      ? -1
      : compareTheme(x, y, sortedBy.slice(1));
  } else if (sortedBy[0] === "minVer") {
    let svComp = semVerCompare(x.min_ver, y.min_ver);
    return svComp === 1
      ? 1
      : svComp === -1
      ? -1
      : sortedBy.length < 2
      ? -1
      : compareTheme(x, y, sortedBy.slice(1));
  } else if (sortedBy[0] === "license") {
    return x.license.localeCompare(y.license) === 1
      ? 1
      : x.license.localeCompare(y.license) === -1
      ? -1
      : sortedBy.length < 2
      ? -1
      : compareTheme(x, y, sortedBy.slice(1));
  }
}

function sortThemes(themeList, sortedBy) {
  themeList.sort((a, b) => compareTheme(a, b, sortedBy));
}
