$(document).ready(function() {

    $('#id_number').addClass("form-control");

    $('#id_model').select2({
        placeholder: "Выберите модель",
        allowClear: true
    });

    $('#id_lighting_object__contract_info__name').select2({
        placeholder: "Выберите ЛНО",
        allowClear: true,
        width: '100%'
    });

});