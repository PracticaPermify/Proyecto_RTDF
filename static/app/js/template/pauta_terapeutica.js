$(document).ready(function() {
    var formularioVisible = false;

    function mostrarFormulario() {
        $("#formulario-pauta").slideDown();
        $("#mostrar-formulario-btn").hide();
        $("#ocultar-formulario-btn").show();
        formularioVisible = true;
        $("html, body").animate({ scrollTop: $("#formulario-pauta").offset().top }, "slow");
    }

    function ocultarFormulario() {
        $("#formulario-pauta").slideUp();
        $("#mostrar-formulario-btn").show();
        $("#ocultar-formulario-btn").hide();
        formularioVisible = false;
    }

    $("#mostrar-formulario-btn").click(function() {
        if (!formularioVisible) {
            mostrarFormulario();
        } else {
            ocultarFormulario();
        }
    });

    $("#ocultar-formulario-btn").click(function() {
        ocultarFormulario();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    let tpTerapiaSelect = document.getElementById('fk_tp_terapia');
    let camposGrbas = document.querySelectorAll('.campos-vocalizacion'); // Nuevos campos para "GRBAS"
    let camposRasati = document.querySelectorAll('.campos-intensidad'); // Nuevos campos para "RASATI"

    function toggleCampos() {
        let selectedTipoInforme = tpTerapiaSelect.selectedOptions[0];

        // Lógica para mostrar u ocultar campos según el tipo de informe
        if (selectedTipoInforme.textContent === 'Vocalización') {
            camposGrbas.forEach(function (campo) {
                campo.style.display = 'block'; // Mostrar campos de "GRBAS"
            });

            camposRasati.forEach(function (campo) {
                campo.style.display = 'none'; // Ocultar campos de "RASATI"
            });
        } else if (selectedTipoInforme.textContent === 'Intensidad') {
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
    tpTerapiaSelect.addEventListener('change', toggleCampos);

    // Llama a la función para configurar los campos según los valores iniciales
    toggleCampos();
});