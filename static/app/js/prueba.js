
    document.addEventListener('DOMContentLoaded', function () {
        const tipoUsuarioSelect = document.getElementById('id_tipo_usuario');
        const pacienteFields = document.getElementById('paciente_fields');
        const familiarFields = document.getElementById('familiar_fields');

        tipoUsuarioSelect.addEventListener('change', function () {
            const selectedOption = tipoUsuarioSelect.value;

            if (selectedOption === 'Paciente') {
                pacienteFields.style.display = 'block';
                familiarFields.style.display = 'none';
            } else if (selectedOption === 'Familiar') {
                pacienteFields.style.display = 'none';
                familiarFields.style.display = 'block';
            } else {
                pacienteFields.style.display = 'none';
                familiarFields.style.display = 'none';
            }
        });
    });
