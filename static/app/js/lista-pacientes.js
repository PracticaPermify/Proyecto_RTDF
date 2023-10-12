const selector=document.getElementById('contenido')


function Form_coeficiente(paciente){
    $.get('/coeficientes_audio/',{
        paciente:paciente},function(FormData){
            selector.innerHTML=FormData;
    })
}
function Form_coeficiente_edit(paciente,audio_id){
    $.get('/coeficientes_audio/',{
        paciente:paciente,id:audio_id},function(FormData){
            document.getElementById('data').innerHTML=FormData;
    })
}

function lista_pacientes(){
    $.get('/lista_pacientes/',{},function(FormData){
            contenido.innerHTML=FormData;
    })
}

lista_pacientes();

function onchangeList(){
    paciente=document.getElementById("paciente").value;
    new_id=document.getElementById("audio-select").value;
    Form_coeficiente_edit(paciente,new_id);

}



