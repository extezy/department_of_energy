$(document).ready(function() {

    $('#id_types__name').select2({
                placeholder: "Выберите тип",
                allowClear: true,
                width: '75%',
            });

    $('#id_names__inventory_number').select2({
        placeholder: "Выберите номер",
        allowClear: true,
        width: '100%'
    });

    $('#id_contract_info__object_number').select2({
        placeholder: "Выберите абонентский номер",
        allowClear: true,
        width: '100%'
    });

    $('#id_contract_info__number').select2({
        placeholder: "Выберите номер",
        allowClear: true,
        width: '100%'
    });

    $('#id_government__department__area__short_name').select2({
        placeholder: "Выберите РУАД",
        allowClear: true,
        width: '75%'
    });

    $('#id_government__department__name').select2({
        placeholder: "Выберите РДО",
        allowClear: true,
        width: '75%'
    });

    $('#id_government__name').select2({
        placeholder: "Выберите г.о.",
        allowClear: true,
        width: '75%'
    });

    $('#id_supplier__name').select2({
        placeholder: "Выберите поставщика",
        allowClear: true,
        width: '75%'
    });

    $('#id_attachment_points__owner__power_grid_organization__name').select2({
        placeholder: "Выберите сетевую организацию",
        allowClear: true,
        width: '75%'
    });

    $('#id_attachment_points__owner__name').select2({
        placeholder: "Выберите владельца точки присоединения",
        allowClear: true,
        width: '75%'
    });

    return false;
});