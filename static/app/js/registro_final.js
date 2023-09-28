document.addEventListener('DOMContentLoaded', function () {
  let tipoUsuarioSelect = document.getElementById('tipo_usuario');
  
  if (tipoUsuarioSelect) {
      tipoUsuarioSelect.addEventListener('change', function () {
          let selectedOption = tipoUsuarioSelect.selectedOptions[0];
          let selectedText = selectedOption.textContent;
          console.log('Seleccionaste:', selectedText);
          
          if (selectedText === 'Paciente') {
              console.log('Realiza lógica para Paciente');
              // Resto de la lógica para Paciente
          } else if (selectedText === 'Familiar') {
              console.log('Realiza lógica para Familiar');
              // Resto de la lógica para Familiar
          }
      });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  let tipoUsuarioSelect = document.getElementById('tipo_usuario');
  let camposPaciente = document.querySelectorAll('.campos-paciente');
  let camposFamiliar = document.querySelectorAll('.campos-familiar'); // Nuevos campos para "Familiar"

  function toggleCampos() {
      let selectedOption = tipoUsuarioSelect.selectedOptions[0];
      let selectedText = selectedOption.textContent;

      if (selectedText === 'Paciente') {
          camposPaciente.forEach(function (campo) {
              campo.style.display = 'block';
          });

          camposFamiliar.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "Familiar"
          });
      } else if (selectedText === 'Familiar') {
          camposPaciente.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "Paciente"
          });

          camposFamiliar.forEach(function (campo) {
              campo.style.display = 'block'; // Mostrar campos de "Familiar"
          });
      } else {
          camposPaciente.forEach(function (campo) {
              campo.style.display = 'none';
          });

          camposFamiliar.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos para otros valores
          });
      }
  }

  tipoUsuarioSelect.addEventListener('change', toggleCampos);

  // Llama a la función para configurar los campos según el valor inicial
  toggleCampos();
});