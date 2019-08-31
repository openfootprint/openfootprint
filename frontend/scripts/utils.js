function pickById(array, id, id_key) {
  if (!array || array.length === 0) return;
  for (var i = 0; i < array.length; i++) {
    if (array[i][id_key || "id"] == id) {
      return array[i];
    }
  }
}

function deleteById(array, id, id_key) {
  if (!array || array.length === 0) return [];
  var newArray = [];
  for (var i = 0; i < array.length; i++) {
    if (array[i][id_key || "id"] != id) {
      newArray.push(array[i]);
    }
  }
  return newArray;
}

function updateById(array, id, id_key, update) {
  if (!array || array.length === 0) return [];
  var newArray = [];
  for (var i = 0; i < array.length; i++) {
    if (array[i][id_key || "id"] != id) {
      newArray.push(array[i]);
    } else {
      newArray.push(Object.assign(array[i], update));
    }
  }
  return newArray;
}

export { pickById, deleteById, updateById };
