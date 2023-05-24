import django_filters
from django import forms
from .models import *


class ElectricityMeterFilter(django_filters.FilterSet):
    ACTIVE_CHOICES = (
        ('True', 'Активный'),
        ('False', 'Выведенный'),
    )

    active = django_filters.MultipleChoiceFilter(
        field_name='active',
        choices=ACTIVE_CHOICES,
        label='Статус',
        widget=forms.CheckboxSelectMultiple()
    )

    type = django_filters.MultipleChoiceFilter(
        field_name='type',
        choices=ElectricityMeter.TYPE_CHOICES,
        label='Тип',
        widget=forms.CheckboxSelectMultiple()
    )

    model = django_filters.ChoiceFilter(
        label='Модель'
    )

    number = django_filters.CharFilter(
        field_name='number',
        label='Номер',
        method='filter_number'
    )

    lighting_object__contract_info__name = django_filters.ChoiceFilter(
        label='Название по контракту'
    )

    def filter_number(self, queryset, number, value):
        if '?' in value:
            values = value.split('?')
            return queryset.filter(number__startswith=values[0], number__endswith=values[1])
        return queryset.filter(number__icontains=value)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Модель
        try:
            self.filters['model'].extra['choices'] = [(o.id, str(o.name)) for o in ElectricityMeterModel.objects.all().distinct()]
        except (KeyError, AttributeError):
            pass

        # Название по контракту
        try:
            self.filters['lighting_object__contract_info__name'].extra['choices'] = [(o.get('name'), str(o.get('name'))) for o in LightingObjectContractInfo.objects.all().values('name').distinct()]
        except (KeyError, AttributeError):
            pass

    class Meta:
        model = ElectricityMeter
        fields = ('active', 'type', 'model')


class LightingFilter(django_filters.FilterSet):

    types__name = django_filters.MultipleChoiceFilter(
        label='Тип объекта'
    )

    names__inventory_number = django_filters.MultipleChoiceFilter(
        label='Инвентарный номер'
    )

    contract_info__object_number = django_filters.ChoiceFilter(
        label='Абонентский номер'
    )

    contract_info__number = django_filters.ChoiceFilter(
        label='Номер контратка'
    )

    government__department__area__short_name = django_filters.ChoiceFilter(
        label='РУАД'
    )

    government__department__name = django_filters.ChoiceFilter(
        label='РДО'
    )

    government__name = django_filters.ChoiceFilter(
        label='г.о.'
    )

    supplier__id = django_filters.ChoiceFilter(
        label='Поставщик ЭЭ'
    )

    attachment_points__owner__power_grid_organization__id = django_filters.ChoiceFilter(
        label='Сетевая организация'
    )

    attachment_points__owner__name = django_filters.ChoiceFilter(
        label='Владелец точки присоединения'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Тип
        try:
            self.filters['types__name'].extra['choices'] = [(o.name, o.name) for o in LightingObjectType.objects.all()]
        except (KeyError, AttributeError):
            pass
        # Инвентарный номер
        try:
            self.filters['names__inventory_number'].extra['choices'] = [(o.get('inventory_number'), str(o.get('inventory_number'))) for o in LightingObjectName.objects.all().values('inventory_number').distinct().order_by('inventory_number')]
        except (KeyError, AttributeError):
            pass
        # Номер контракта
        try:
            self.filters['contract_info__number'].extra['choices'] = [(o.get('number'), str(o.get('number'))) for o in LightingObjectContractInfo.objects.all().values('number').distinct().order_by('number')]
        except (KeyError, AttributeError):
            pass

        # Номер абонента в контракте
        try:
            self.filters['contract_info__object_number'].extra['choices'] = [(o.get('object_number'), str(o.get('object_number'))) for o in LightingObjectContractInfo.objects.all().values('object_number').distinct().order_by('object_number')]
        except (KeyError, AttributeError):
            pass

        # РУАД
        try:
            self.filters['government__department__area__short_name'].extra['choices'] = [(o.short_name, str(o.short_name) + '. ' + o.name) for o in Area.objects.all().order_by('short_name')]
        except (KeyError, AttributeError):
            pass

        # РДО
        try:
            self.filters['government__department__name'].extra['choices'] = [(o.name, str(o.name)) for o in DistrictRoadDepartment.objects.all()]
        except (KeyError, AttributeError):
            pass

        # Г.О.
        try:
            self.filters['government__name'].extra['choices'] = [(o.name, str(o.name)) for o in LocalGovernment.objects.all()]
        except (KeyError, AttributeError):
            pass

        # Поставщик ЭЭ
        try:
            self.filters['supplier__id'].extra['choices'] = [(o.id, str(o.name)) for o in Supplier.objects.all()]
        except (KeyError, AttributeError):
            pass

        # Сетевая организация
        try:
            self.filters['attachment_points__owner__power_grid_organization__id'].extra['choices'] = [(o.id, str(o.name)) for o in PowerGridOrganization.objects.all()]
        except (KeyError, AttributeError):
            pass

        # Владелец точки присоединения
        try:
            self.filters['attachment_points__owner__name'].extra['choices'] = [(o.name, str(o.name)) for o in AttachmentPointOwner.objects.all()]
        except (KeyError, AttributeError):
            pass

    class Meta:
        model = LightingObject
        fields = ('types',)
