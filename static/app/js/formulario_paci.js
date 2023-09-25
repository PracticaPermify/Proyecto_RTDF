document.addEventListener('DOMContentLoaded', function () {
  let tipoUsuarioSelect = document.getElementById('tipo_usuario');
  let camposgrbas = document.querySelectorAll('.campos-grbas');
  let camposrasati = document.querySelectorAll('.campos-rasati'); // Nuevos campos para "Familiar"

  function toggleCampos() {
      let selectedOption = tipoUsuarioSelect.selectedOptions[0];
      let selectedText = selectedOption.textContent;

      if (selectedText === 'Paciente') {
          camposgrbas.forEach(function (campo) {
              campo.style.display = 'block';
          });

          camposrasati.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "Familiar"
          });
      } else if (selectedText === 'Familiar') {
          camposgrbas.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "Paciente"
          });

          camposrasati.forEach(function (campo) {
              campo.style.display = 'block'; // Mostrar campos de "Familiar"
          });
      } else {
          camposgrbas.forEach(function (campo) {
              campo.style.display = 'none';
          });

          camposrasati.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos para otros valores
          });
      }
  }

  tipoUsuarioSelect.addEventListener('change', toggleCampos);

  // Llama a la función para configurar los campos según el valor inicial
  toggleCampos();
});