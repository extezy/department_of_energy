from django.contrib import admin
from .models import *


class PowerEngineerInline(admin.TabularInline):
    """Определяет формат вставки PowerEngineer (Используется в AreaAdmin)"""
    model = PowerEngineer
    extra = 0


class EmployeeInline(admin.TabularInline):
    """Определяет формат вставки Employee (Используется в AttachmentPointOwnerAdmin)"""
    model = Employee
    extra = 0


class DistrictRoadDepartmentInline(admin.TabularInline):
    """Определяет формат вставки DistrictRoadDepartment (Используется в AreaAdmin)"""
    model = DistrictRoadDepartment
    extra = 0


class LocalGovernmentInline(admin.TabularInline):
    """Определяет формат вставки LocalGovernment (Используется в DistrictRoadDepartmentAdmin)"""
    model = LocalGovernment
    extra = 0


class ElectricityMeterInline(admin.TabularInline):
    """Определяет формат вставки ElectricityMeter (Используется в LightingObject)"""
    model = ElectricityMeter
    extra = 0
    # raw_id_fields = ('lighting_object',)


class LightingObjectDocumentInline(admin.TabularInline):
    """Определяет формат вставки LightingObjectDocument (Используется в LightingObject)"""
    model = LightingObjectDocument
    extra = 0


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'second_phone_number', 'email')
    search_fields = ['name']
    list_filter = ('name',)
    list_per_page = 30


@admin.register(PowerEngineer)
class PowerEngineerAdmin(admin.ModelAdmin):
    list_display = ('verbose_name', 'phone_number', 'area')
    search_fields = ['verbose_name']
    list_filter = ('verbose_name',)
    list_per_page = 15


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ['name']
    list_filter = ('name',)
    list_per_page = 30

    inlines = [PowerEngineerInline, DistrictRoadDepartmentInline]


@admin.register(DistrictRoadDepartment)
class DistrictRoadDepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'area')
    search_fields = ['name', 'area__name']
    list_filter = ('area',)
    list_per_page = 30

    inlines = [LocalGovernmentInline]


@admin.register(LocalGovernment)
class LocalGovernmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'department')
    search_fields = ('name',)
    list_filter = ('department',)
    list_per_page = 30


@admin.register(ElectricityMeterModel)
class ElectricityMeterTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'life_time')
    search_fields = ['name']
    list_filter = ('name',)
    list_per_page = 30


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ('latitude', 'longitude')
    list_per_page = 30


@admin.register(InstallationLocation)
class InstallationLocationAdmin(admin.ModelAdmin):
    list_display = ('place', 'coordinate')
    search_fields = ['place']
    list_filter = ('place',)
    list_per_page = 30


@admin.register(LightingObjectType)
class LightingObjectTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']
    list_per_page = 10


@admin.register(LightingObjectName)
class LightingObjectNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'inventory_number', 'inspection_report')
    search_fields = ['name', 'inventory_number']
    list_per_page = 30


@admin.register(LightingObjectContractInfo)
class LightingObjectContractInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'object_number')
    list_filter = ('number', )
    search_fields = ('name', 'number', 'object_number')
    list_per_page = 30


@admin.register(LightingObjectDocument)
class LightingObjectDocumentAdmin(admin.ModelAdmin):
    list_display = ('lighting_object', 'connection_act', 'support_scheme', 'single_line_scheme')
    search_fields = ['lighting_object']
    autocomplete_fields = ['lighting_object']
    list_per_page = 25


@admin.register(AttachmentPointOwner)
class AttachmentPointOwnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'second_phone_number', 'email')
    search_fields = ['name']
    list_per_page = 25

    inlines = [EmployeeInline]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('position', 'name', 'phone_number', 'email', 'attachmentpointowner')
    search_fields = ['position', 'attachmentpointowner']
    autocomplete_fields = ['attachmentpointowner', ]
    list_per_page = 30


@admin.register(LightingObject)
class LightingObjectAdmin(admin.ModelAdmin):
    list_display = ('contract_info', 'government', 'supplier', 'power', 'note')
    list_filter = ('government__department__area', 'supplier')
    filter_horizontal = ('types', 'names', 'substations', 'attachment_points')
    search_fields = ['contract_info__name', 'contract_info__number', 'contract_info__object_number', 'names__name', 'names__inventory_number', 'note']
    autocomplete_fields = ['contract_info', 'government', 'supplier']
    list_per_page = 20

    inlines = [ElectricityMeterInline]


@admin.register(Substation)
class SubstationAdmin(admin.ModelAdmin):
    list_display = ('number', 'coordinates')
    search_fields = ['number']
    list_per_page = 30

    inlines = [ElectricityMeterInline]


@admin.register(PowerGridOrganization)
class PowerGridOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name']
    list_per_page = 30


@admin.register(AttachmentPoint)
class AttachmentPointAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'coordinates')
    search_fields = ['name', 'owner__name']
    autocomplete_fields = ['owner', ]
    list_per_page = 25

    inlines = [ElectricityMeterInline]


@admin.register(ElectricityMeter)
class ElectricityMeterAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'type', 'active', 'check_date', 'model', 'transformation_ratios', 'coordinates', 'admission_electricity_meter_act', 'seals', 'installation_location')
    list_filter = ('type', 'model')
    ordering = ('check_date',)
    search_fields = ['number', 'model__name']
    autocomplete_fields = ['model', 'installation_location', 'lighting_object', 'substation', 'attachment_point']
    list_per_page = 25


@admin.register(BreezePoint)
class BreezePointAdmin(admin.ModelAdmin):
    list_display = ('number', 'ip', 'iccid', 'coordinates', 'note', 'lighting_object')
    ordering = ('number',)
    search_fields = ['number', 'ip', 'iccid']
    autocomplete_fields = ['lighting_object',]
    list_per_page = 25


@admin.register(CarouselFile)
class CarouselFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo')
