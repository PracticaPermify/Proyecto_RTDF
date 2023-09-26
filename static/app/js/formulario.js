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
  let rasatiFields = document.getElementById('rasati-fields');
  let grbasFields = document.getElementById('grbas-fields');

  if (tpInformeSelect && rasatiFields && grbasFields) {
      tpInformeSelect.addEventListener('change', function () {
          let selectedValue = tpInformeSelect.value;

          // Oculta todos los campos primero
          rasatiFields.style.display = 'none';
          grbasFields.style.display = 'none';

          // Luego, muestra los campos según la opción seleccionada
          if (selectedValue === 'RASATI') {
              rasatiFields.style.display = 'block';
          } else if (selectedValue === 'GRBAS') {
              grbasFields.style.display = 'block';
          }
      });
  }
});