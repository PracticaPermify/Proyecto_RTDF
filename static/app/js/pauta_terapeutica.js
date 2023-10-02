
$(document).ready(function() {
    var formularioVisible = false;

    $("#mostrar-formulario-btn").click(function() {
        if (formularioVisible) {
            // Si el formulario ya está visible, ocúltalo y cambia el mensaje del botón
            $("#formulario-pauta").slideUp();
            $("#mostrar-formulario-btn").text("Agregar nueva pauta terapéutica");
            formularioVisible = false;

            $("#mostrar-formulario-btn").removeClass("btn-danger").addClass("btn-primary");

            // Limpia los campos del formulario
            $("#formulario-pauta input[type='text']").val("");
            $("#formulario-pauta textarea").val("");
            $("#formulario-pauta select").val("");


        } else {
            // Si el formulario no está visible, muéstralo y cambia el mensaje del botón
            $("#formulario-pauta").slideDown();
            $("#mostrar-formulario-btn").text("Descartar la nueva pauta terapéutica");
            formularioVisible = true;

            //cambio de las clases del boton usan bootstrap
            $("#mostrar-formulario-btn").removeClass("btn-primary").addClass("btn-danger");
              // Limpia los campos del formulario
            $("#formulario-pauta input[type='text']").val("");
            $("#formulario-pauta textarea").val("");
            $("#formulario-pauta select").val("");

            //ajustar el scroll al desplegar el formulario
            $("html, body").animate({ scrollTop: $("#formulario-pauta").offset().top }, "slow");
        }



    });

    $("#ocultar-formulario-btn").click(function() {
        if (formularioVisible) {
            // Si el formulario ya está visible, ocúltalo y cambia el mensaje del botón
            $("#formulario-pauta").slideUp();
            $("#ocultar-formulario-btn").text("Descartar la nueva pauta terapéutica");
            $("#mostrar-formulario-btn").text("Agregar nueva pauta terapéutica");
            $("#mostrar-formulario-btn").removeClass("btn-danger").addClass("btn-primary");
            formularioVisible = false;
    
                // Limpia los campos del formulario
            $("#formulario-pauta input[type='text']").val("");
            $("#formulario-pauta textarea").val("");
            $("#formulario-pauta select").val("");
    
    
        }
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