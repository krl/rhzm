function $(id) {
  return document.getElementById(id)
}

function show(id) {
  $(id).style.display = "inline";
  return false;
}

function hide(id) {
  $(id).style.display = "none";
  return false;
}