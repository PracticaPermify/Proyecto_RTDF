// Variables globales para manejar la grabación de audio
let audioContext;
let audioRecorder;
let audioChunks = [];

document.querySelector('#start-stop').addEventListener('click', async function () {

    var csrftoken = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]').value;

    if (!audioRecorder) {
        // Iniciar la grabación si aún no se ha iniciado
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            audioRecorder = new MediaRecorder(stream);

            audioRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    audioChunks.push(event.data);
                }
            };

            audioRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const formData = new FormData();
                formData.append('audio', audioBlob);

                // Enviar el archivo de audio al servidor
                fetch(vocalizacionConPautaURL, {
                    method: 'POST',
                    body: formData,
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                })
                .then(response => {
                    if (response.ok) {
                        console.log('Grabación de audio completada y enviada al servidor.');
                    } else {
                        console.error('Error al enviar el audio al servidor.');
                    }
                });
            };

            audioRecorder.start();
            document.querySelector('#start-stop').textContent = 'Detener Grabación';
        } catch (error) {
            console.error('Error al acceder al micrófono: ', error);
        }
    } else {
        // Detener la grabación si ya se inició
        audioRecorder.stop();
        audioRecorder = null;
        audioChunks = [];
        audioContext.close().then(() => {
            document.querySelector('#start-stop').textContent = 'Empezar Grabación';
        });
    }
});
