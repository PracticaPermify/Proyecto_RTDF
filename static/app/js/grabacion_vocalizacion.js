document.querySelector('.start-stop').addEventListener('click', function () {

    console.log("El valor de bpm es: " + window.id); //
    var pauta_id = window.id;

    
    var csrftoken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;
    // url de la vista vocalizacion
    var url;
    if (pauta_id) {
        url = vocalizacionConPautaURL;
    } else {
        url = vocalizacionURL;
    }

    // solicitud POST a la URL construida
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken
        },
    }).then(function (response) {
        if (response.ok) {
            console.log('Grabación de audio completada.');
        } else {
            console.error('Error al grabar audio.');
        }
    });
});