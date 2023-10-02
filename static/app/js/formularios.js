document.addEventListener('DOMContentLoaded', function () {
  let tipoUsuarioSelect = document.getElementById('tp_informe');
  
  if (tipoUsuarioSelect) {
      tipoUsuarioSelect.addEventListener('change', function () {
          let selectedOption = tipoUsuarioSelect.selectedOptions[0];
          let selectedText = selectedOption.textContent;
          console.log( selectedText);
          
          if (selectedText === 'GRBAS') {
              console.log('Seleccionaste GRBAS para formulario');
          } else if (selectedText === 'RASATI') {
              console.log('Seleccionaste RASATI para formulario');
          }
      });
  }
});

document.addEventListener('DOMContentLoaded', function () {
  let tpInformeSelect = document.getElementById('tp_informe');
  let camposGrbas = document.querySelectorAll('.campos-grbas'); // Nuevos campos para "GRBAS"
  let camposRasati = document.querySelectorAll('.campos-rasati'); // Nuevos campos para "RASATI"

  function toggleCampos() {
      let selectedTipoInforme = tpInformeSelect.selectedOptions[0];

      // Lógica para mostrar u ocultar campos según el tipo de informe
      if (selectedTipoInforme.textContent === 'GRBAS') {
          camposGrbas.forEach(function (campo) {
              campo.style.display = 'block'; // Mostrar campos de "GRBAS"
          });

          camposRasati.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "RASATI"
          });
      } else if (selectedTipoInforme.textContent === 'RASATI') {
          camposGrbas.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos de "GRBAS"
          });

          camposRasati.forEach(function (campo) {
              campo.style.display = 'block'; // Mostrar campos de "RASATI"
          });
      } else {
          camposGrbas.forEach(function (campo) {
              campo.style.display = 'none';
          });

          camposRasati.forEach(function (campo) {
              campo.style.display = 'none'; // Ocultar campos para otros valores de informe
          });
      }
  }
  tpInformeSelect.addEventListener('change', toggleCampos);

  // Llama a la función para configurar los campos según los valores iniciales
  toggleCampos();
});