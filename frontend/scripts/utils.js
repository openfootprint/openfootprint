
function pickById(array, id, id_key) {
  if (!array || array.length === 0) return;
  for (var i=0;i<array.length;i++) {
      if (array[i][id_key||"id"] == id) {
          return array[i];
      }
  }
}

export {
  pickById
}