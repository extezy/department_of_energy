from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from department_of_energy.settings import STATIC_ROOT
from django.core.files.storage import FileSystemStorage


class PowerGridOrganization(models.Model):
    """
    Класс для представления Сетевой организации к которой относятся поставщики электроэнергии
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название организации', help_text='Название организации')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Сетевая организация'
        verbose_name_plural = 'Сетевые организации'

    def __str__(self):
        return self.name


class Supplier(models.Model):
    """
    Класс для представления поставщика электроэнергии
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название организации', help_text='Название организации')
    phone_number = PhoneNumberField(blank=True, verbose_name='Телефон', help_text='Контактный телефон')
    second_phone_number = PhoneNumberField(blank=True, verbose_name='Второй телефон', help_text='Второй телефон')
    email = models.EmailField(blank=True, verbose_name='Электронная почта', help_text='Электронная почта')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Поставщик электроэнергии'
        verbose_name_plural = 'Поставщики электроэнергии'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Нет названия'


class Area(models.Model):
    """
    Класс для представления РУАД
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название', help_text='Название РУАД (Можайский)')
    short_name = models.PositiveSmallIntegerField(verbose_name='Номер РУАД', help_text='Номер РУАД')

    class Meta:
        ordering = ('name',)
        verbose_name = 'РУАД'
        verbose_name_plural = 'РУАДы'

    def __str__(self):
        return self.name

    # TODO Может можно убрать вызов этого метода
    def get_power_engineers(self, obj):
        return obj.engineers.all


class DistrictRoadDepartment(models.Model):
    """
    Модель для представления районно дорожного отдела (РДО)
    """
    name = models.CharField(unique=True, max_length=255, verbose_name='Название', help_text='Название РДО (Домодедовское)')
    area = models.ForeignKey(Area, verbose_name='РУАД', on_delete=models.CASCADE, related_name='departments')

    class Meta:
        verbose_name = 'РДО'
        verbose_name_plural = 'РДО'

    def __str__(self):
        return self.name


class LocalGovernment(models.Model):
    """
    Модель для представления органа местного самоуправления (ОМС)
    """
    name = models.CharField(max_length=255, verbose_name='Название', help_text='Название ОМС (г.о. Домодедово)')
    department = models.ForeignKey(DistrictRoadDepartment, verbose_name='ОМС', on_delete=models.CASCADE, related_name='governments')

    class Meta:
        verbose_name = 'ОМС'
        verbose_name_plural = 'ОМС'

    def __str__(self):
        return self.name


class PowerEngineer(models.Model):
    """
    Модель для представления контактных данных энергетика
    """
    verbose_name = models.CharField(max_length=70, verbose_name='ФИО', help_text='ФИО')
    phone_number = PhoneNumberField(verbose_name='Телефон', blank=True)
    area = models.OneToOneField(Area, verbose_name='РУАД', null=True, on_delete=models.SET_NULL, related_name='engineers')

    class Meta:
        verbose_name = 'Энергетик'
        verbose_name_plural = 'Энергетики'

    def __str__(self):
        return self.verbose_name


class ElectricityMeterModel(models.Model):
    """
    Класс для представления Модели счетчика
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='Модель счётчика', help_text='Модель счётчика (Меркурий 27)')
    life_time = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Сколько лет до поверки', help_text='Через сколько лет требуется поверка')  # Срок службы до следующей поверки

    class Meta:
        verbose_name = 'Модель счетчика'
        verbose_name_plural = 'Модели счетчиков'

    def __str__(self):
        return self.name

    def get_lifetime(self):
        if self.life_time is not None:
            return self.life_time
        else:
            return 0


class Coordinate(models.Model):
    """
    Класс для представления координат на карте
    """
    latitude = models.FloatField(verbose_name='Широта', help_text='Широта')  # Широта
    longitude = models.FloatField(verbose_name='Долгота', help_text='Долгота')  # Долгота

    class Meta:
        unique_together = ('latitude', 'longitude')
        verbose_name = 'Координаты'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return str(self.longitude) + "," + str(self.latitude)


class InstallationLocation(models.Model):
    """
    Класс для представления места установки
    """
    place = models.CharField(max_length=100, verbose_name='Место установки', help_text='Место установки')
    coordinate = models.ForeignKey(Coordinate, verbose_name='Координаты', blank=True, null=True, default=None,
                                   on_delete=models.SET_NULL)  # Координаты

    class Meta:
        verbose_name = 'Место установки'
        verbose_name_plural = 'Места установки'
        unique_together = ('place', 'coordinate')

    def __str__(self):
        return self.place


class LightingObjectContractInfo(models.Model):
    """
    Модель для представления идентификационных данных по контракту для объектов освещения
    """
    name = models.CharField(null=True, blank=True, max_length=255, verbose_name='Название по контракту', help_text='Название по контракту')  # Имя по контракту
    number = models.CharField(max_length=50, verbose_name='Номер контракта', help_text='Номер контракта')
    object_number = models.CharField(max_length=50, verbose_name='Номер объекта в контракте')

    class Meta:
        unique_together = ('name', 'number', 'object_number')
        verbose_name = 'Информация по контракту'
        verbose_name_plural = 'Информация по контракту'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return 'Не внесено название из контракта'


class AttachmentPointOwner(models.Model):
    """
    Класс для представления объекта владельца точки присоединения
    """
    name = models.CharField(max_length=255, unique=True, verbose_name='Название организации', help_text='Название организации')
    phone_number = PhoneNumberField(blank=True, verbose_name='Телефон', help_text='Контактный телефон')
    second_phone_number = PhoneNumberField(blank=True, verbose_name='Второй телефон', help_text='Второй телефон')
    email = models.EmailField(blank=True, verbose_name='Электронная почта', help_text='Электронная почта')
    power_grid_organization = models.ForeignKey(PowerGridOrganization, blank=True, null=True, verbose_name='Сетевая организация',
                                                on_delete=models.CASCADE, related_name='owners')

    class Meta:
        verbose_name = 'Владелец точки присоединения'
        verbose_name_plural = 'Владелецы точек присоединения'

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Класс для представления работника сетевой организации
    """
    position = models.CharField(max_length=40, verbose_name='Должность', help_text='Должность')
    name = models.CharField(max_length=50, verbose_name='ФИО', help_text='ФИО')
    phone_number = PhoneNumberField(blank=True, verbose_name='Телефон', help_text='Контактный телефон')
    # second_phone_number = PhoneNumberField(blank=True, verbose_name='Второй телефон', help_text='Второй телефон')
    email = models.EmailField(blank=True, verbose_name='Электронная почта', help_text='Электронная почта')
    attachmentpointowner = models.ForeignKey(AttachmentPointOwner, null=True, on_delete=models.SET_NULL, verbose_name='Сетевая организация',
                                 related_name='employees')

    class Meta:
        verbose_name = 'Сотрудник сетевой организации'
        verbose_name_plural = 'Сотрудники сетевой организации'

    def __str__(self):
        return self.name


class Substation(models.Model):
    """
    Класс представления трансформаторной подстанции
    """

    number = models.CharField(max_length=75, verbose_name='Номер ТП')  # Номер ТП
    power = models.FloatField(blank=True, null=True, verbose_name='Максимальная мощность')  # Максимальная мощность
    coordinates = models.ForeignKey(Coordinate, verbose_name='Координаты', on_delete=models.SET_NULL, blank=True,
                                    null=True, default=None)  # Координаты

    class Meta:
        unique_together = ('number', 'coordinates')
        verbose_name = 'Трансформаторная подстанция'
        verbose_name_plural = 'Трансформаторные подстанции'

    def __str__(self):
        return str(self.number)


class AttachmentPoint(models.Model):
    """
    Класс для представления объекта точки присоединения
    """

    name = models.CharField(max_length=255, verbose_name='Точка присоединения', help_text='ВЛ, КЛ, РУ... от ТП')
    power = models.FloatField(blank=True, null=True, verbose_name='Максимальная мощность')  # Максимальная мощность
    owner = models.ForeignKey(AttachmentPointOwner,
                              null=True, blank=True,
                              on_delete=models.SET_NULL,
                              verbose_name='Владелец точки присоединения',
                              related_name='attachment_points')  # Владелец точки присоединения
    coordinates = models.ForeignKey(Coordinate, verbose_name='Координаты', on_delete=models.SET_NULL, blank=True, null=True, default=None)  # Координаты

    class Meta:
        unique_together = ('name', 'coordinates')
        verbose_name = 'Точка присоединения'
        verbose_name_plural = 'Точки присоединения'

    def __str__(self):
        return self.name


class LightingObjectType(models.Model):
    """
    Класс для представления типа объекта освещения
    """
    name = models.CharField(unique=True, max_length=100, verbose_name='Тип объекта освещения', help_text='Тип объекта освещения')

    class Meta:
        verbose_name = 'Тип объекта освещения'
        verbose_name_plural = 'Типы объектов освещения'

    def __str__(self):
        return self.name


class LightingObjectName(models.Model):
    """
    Модель для представления идентификационных данных по бухгалтерской справке для объектов освещения
    """
    name = models.CharField(max_length=255, verbose_name='Название объекта на балансе',
                            help_text='Название объекта на балансе')  # Имя объекта
    inventory_number = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='Инвентарный номер (Балансовый)',
                                                   help_text='Инвентарный номер (Балансовый)')  # Инвентарный номер

    inspection_report = models.FileField(blank=True, upload_to='inspection_report_act/',
                                                       verbose_name='Акт осмотра ЛНО',
                                                       help_text='PDF файл акта осмотра ЛНО')  # ПФД Объект акта осмотра


    class Meta:
        unique_together = ('name', 'inventory_number')
        verbose_name = 'Информация по балансу'
        verbose_name_plural = 'Информация по балансу'

    def __str__(self):
        return self.name


class LightingObject(models.Model):
    """
    Класс для представления объекта освещения
    """
    types = models.ManyToManyField(LightingObjectType, verbose_name='Типы объекта', related_name='lighting_objects')
    contract_info = models.ForeignKey(LightingObjectContractInfo, blank=True, verbose_name='Название объекта по контракту', on_delete=models.DO_NOTHING)     # Идентификационные данные объекта
    names = models.ManyToManyField(LightingObjectName, blank=True, verbose_name='Название объекта на балансе', related_name='lighting_objects')
    government = models.ForeignKey(LocalGovernment, blank=True, null=True, verbose_name='ОМС', on_delete=models.SET_NULL, related_name='lighting_objects')  # ОМС
    supplier = models.ForeignKey(Supplier, null=True, verbose_name='Поставщик электроэнергии', on_delete=models.SET_NULL, related_name='lighting_objects') # Поставщик электроэнергии
    power = models.FloatField(blank=True, null=True, verbose_name='Максимальная мощность')  # Максимальная мощность
    note = models.TextField(blank=True, null=True, default=None, verbose_name='Примечание')   # Примечание
    substations = models.ManyToManyField(Substation, blank=True, verbose_name='ТП',  related_name='lighting_objects')
    attachment_points = models.ManyToManyField(AttachmentPoint, blank=True, verbose_name='Точки присоединения', related_name='lighting_objects')

    class Meta:
        verbose_name = 'Объект освещения'
        verbose_name_plural = '!Объекты освещения'

    def __str__(self):
        return str(self.contract_info)

    def add_power_from_excel(obj, excel_power):
        if obj.power:
            obj.power += float(excel_power)
        else:
            obj.power = excel_power

    def get_data_for_excel(self, obj):
        excel_data = {}
        types = [type_value.name for type_value in obj.types.all()]
        excel_data['Тип'] = ', '.join(types)

        excel_data['Название по контракту'] = obj.contract_info.name
        excel_data['Номер контракта'] = str(obj.contract_info.number)
        excel_data['Номер в контракте'] = str(obj.contract_info.object_number)

        if obj.names:
            balance_names = [balance.name + ':' + str(balance.inventory_number) for balance in obj.names.all()]
            excel_data['На балансе'] = '\n '.join(balance_names)

        excel_data['Городской округ'] = str(obj.government.name or '')
        excel_data['РДО'] = str(obj.government.department.name or '')
        excel_data['РУАД'] = str(obj.government.department.area.name or '')

        if obj.supplier:
            excel_data['Поставщик электроэнергии'] = str(obj.supplier.name or '')

        excel_data['Мощность'] = str(obj.power or '')

        if obj.meters:
            lighting_electricity_meters = [meter.type + ':' + str(meter.number) + ':' + meter.model.name for meter in obj.meters.filter(active=True)]
            excel_data['Счётчики электроэнергии'] = ';\n '.join(lighting_electricity_meters)

        if obj.substations:
            substation_points = [str(substation.number or '') + ':' + str(substation.power or '') + ':' + str(substation.coordinates or '') for substation in obj.substations.all()]
            excel_data['ТП'] = ';\n '.join(substation_points)

        if obj.attachment_points:
            lighting_attachment_point = [str(attachment.name or '') + ':' + str(attachment.power or '') + ':' + ':' + str(attachment.coordinates or '') for attachment in
                                 obj.attachment_points.all()]
            excel_data['Точки присоединения'] = ';\n '.join(lighting_attachment_point)

        excel_data['Примечание'] = obj.note

        return excel_data

    def get_electricitymeter(self, obj):
        return obj.meters.all

    def get_substations(self, obj):
        return obj.substations.all

    def get_government(self):
        if self.government is not None:
            return self.government.id
        else:
            return '0'

    def get_supplier(self):
        if self.supplier is not None:
            return self.supplier.id
        else:
            return '0'

    def get_contract_info(self):
        return self.contract_info.id

    def get_contract_number(self):
        if self.contract_info.number is not None:
            return self.contract_info.number.id
        else:
            return '0'


class BreezePoint(models.Model):
    """
        Класс для представления БРИЗа
    """

    number = models.CharField(max_length=50, verbose_name='Номер АППНО', help_text='Номер')
    ip = models.GenericIPAddressField(verbose_name='IP адрес', help_text='IP адрес')
    iccid = models.CharField(max_length=25, verbose_name='Номер сим карты', help_text='Номер сим карты(ICCID)')
    coordinates = models.ForeignKey(Coordinate, verbose_name='Координаты шкафа', blank=True, null=True,
                                    on_delete=models.SET_NULL)  # Координаты
    note = models.TextField(blank=True, null=True, default=None, verbose_name='Примечание')   # Примечание
    lighting_object = models.ForeignKey(LightingObject, verbose_name='Объект освещения', blank=True, null=True,
                                        on_delete=models.SET_NULL, related_name='breeze_points')

    class Meta:
        ordering = ('id',)
        verbose_name = 'Шкаф БРИЗ'
        verbose_name_plural = 'Шкафы БРИЗ'


class ElectricityMeter(models.Model):
    """
    Класс для представления счетчика электроэнергии
    """

    TYPE_CHOICES = [
        ('Контрольный', 'Контрольный'),
        ('Расчётный', 'Расчётный')
    ]

    active = models.BooleanField(default=True, verbose_name='В эксплуатации')
    type = models.CharField(choices=TYPE_CHOICES, default='Расчётный', verbose_name='Тип счётчика',
                            help_text='Контрольный, Расчётный', max_length=20)  # Тип счётчика
    number = models.CharField(max_length=50, verbose_name='Номер счётчика', help_text='Номер')  # Номер счётчика
    check_date = models.DateField(blank=True, null=True, verbose_name='Дата последней поверки', help_text='Дата поверки')  # Дата поверки
    model = models.ForeignKey(ElectricityMeterModel, null=True, verbose_name='Модель счётчика', on_delete=models.SET_NULL)  # Модель счётчика
    transformation_ratios = models.CharField(max_length=100, null=True, blank=True, verbose_name='Коэффициенты трансформации', help_text='ТТ/ТН')
    coordinates = models.ForeignKey(Coordinate, verbose_name='Координаты', blank=True, null=True,  on_delete=models.SET_NULL)  # Координаты
    seals = models.TextField(blank=True, null=True, verbose_name='Номера пломб с описанием', help_text='Пломба 1523, 7594...')  # Пломбы
    installation_location = models.ForeignKey(InstallationLocation, verbose_name='Место установки', blank=True, null=True, default=None,  on_delete=models.SET_NULL)    # Место установки
    admission_electricity_meter_act = models.FileField(blank=True, upload_to='admission_electricity_meter_act/',
                                                       verbose_name='Акт допуска прибора учета',
                                                       help_text='PDF файл акта допуска прибора учета')  # ПФД Объект акта допуска прибора учета
    lighting_object = models.ForeignKey(LightingObject, verbose_name='Объект освещения', blank=True, null=True,
                                        on_delete=models.SET_NULL, related_name='meters')
    substation = models.ForeignKey(Substation, verbose_name='Трансформаторная подстанция', blank=True, null=True,
                                        on_delete=models.SET_NULL, related_name='meters')  # Трансформаторная подстанция
    attachment_point = models.ForeignKey(AttachmentPoint, verbose_name='Точка присоединения', blank=True, null=True,
                                        on_delete=models.SET_NULL, related_name='meters')  # Точка присоединения

    class Meta:
        ordering = ('id',)
        verbose_name = 'Счетчик электроэнергии'
        verbose_name_plural = '!Счетчики электроэнергии'

    def __str__(self):
        return str(self.number)

    def get_location(self):
        return self.installation_location

    def get_absolute_url(self):
        return reverse('electricitymeter_detail', args=[str(self.id)])

    def get_lifetime(self):
        # TODO посчитать год очередной поверки
        if self.check_date is not None:
            return int(self.check_date.strftime("%Y")) + self.model.get_lifetime()
        else:
            return 2000

    def get_active(self):
        if self.active:
            return 'Да'
        else:
            return 'Нет'


class LightingObjectDocument(models.Model):
    """
    Модель для представления документов на объект
    """
    lighting_object = models.OneToOneField(LightingObject, null=True, related_name='documents', default=None, verbose_name='Объект освещения', on_delete=models.SET_NULL) # Какому объекту принадлежат документы
    connection_act = models.FileField(blank=True, null=True, default=None, upload_to='technical_acts/',
                                      verbose_name='Акт тех. присоединения',
                                      help_text='PDF файл акта тех. присоединения')  # ПФД Объект акта тех присоединения
    support_scheme = models.FileField(blank=True, null=True, default=None, upload_to='support_scheme/',
                                      verbose_name='Поопорная схема',
                                      help_text='PDF файл акта поопорной схемы')  # ПДФ Объект поопорной схемы
    single_line_scheme = models.FileField(blank=True, null=True, default=None, upload_to='single_line_scheme/',
                                          verbose_name='Однолинейная схема',
                                      help_text='PDF файл однолинейной схемы')  # ПДФ Объект однолинейной схемы

    class Meta:
        verbose_name = 'Пакет документации'
        verbose_name_plural = 'Пакеты документации'

    def __str__(self):
        return str(self.lighting_object)


fs = FileSystemStorage(location=STATIC_ROOT)


class CarouselFile(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True, verbose_name='Описание', help_text='JPG файл')
    photo = models.FileField(blank=True, null=True, default=None, upload_to='home_img/',
                             verbose_name='Картинка для главной страницы',
                             help_text='JPG файл ',
                             storage=fs
                             )

    def delete(self, *args, **kwargs):
        self.photo.storage.delete(self.photo.name)
        super().delete()

    def __str__(self):
        return self.photo.path

    class Meta:
        verbose_name = 'Картинка для главной страницы'
        verbose_name_plural = 'Картинки для главной страницы'
