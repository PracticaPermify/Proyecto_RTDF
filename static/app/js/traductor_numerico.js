document.addEventListener("DOMContentLoaded", function() {
  // Función para traducir el valor
  function traducirValor(valor) {
      var traducciones = {
          0: 'Normal',
          1: 'Alteración leve',
          2: 'Alteración moderada',
          3: 'Alteración severa',
      };
      return traducciones[valor] || valor;
  }

  // Obtener todas las celdas que contienen valores a traducir
  var celdasTraducir = document.querySelectorAll('.valor-traducir');

  // Iterar sobre las celdas y traducir los valores
  celdasTraducir.forEach(function(celda) {
      var valorOriginal = celda.textContent;
      var valorTraducido = traducirValor(parseInt(valorOriginal));
      celda.textContent = valorTraducido;
  });
});