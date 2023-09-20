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

    function toggleCamposPaciente() {
        let selectedOption = tipoUsuarioSelect.selectedOptions[0];
        let selectedText = selectedOption.textContent;

        if (selectedText === 'Paciente') {
            camposPaciente.forEach(function (campo) {
                campo.style.display = 'block';
            });
        } else {
            camposPaciente.forEach(function (campo) {
                campo.style.display = 'none';
            });
        }
    }

    tipoUsuarioSelect.addEventListener('change', toggleCamposPaciente);

    // Llama a la función para configurar los campos según el valor inicial
    toggleCamposPaciente();
});