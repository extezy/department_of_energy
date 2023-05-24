from django.db.models.functions import Cast
from django.db.models import CharField
from django.views.generic import\
    ListView, DetailView, FormView
from django.http import HttpResponse
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import *
from .filters import LightingFilter, ElectricityMeterFilter



class CarouselListView(ListView):
    model = CarouselFile
    template_name = 'home.html'


class DetailsAjaxView(FormView):
    pass


class AttachmentPointDetailView(DetailView):
    model = AttachmentPoint
    template_name = 'attachmentpoint_detail.html'


class AttachmentPointOwnerListView(ListView):
    model = AttachmentPointOwner
    template_name = 'attachment_point_owner.html'


class PowerGridOrganizationListView(ListView):
    model = PowerGridOrganization
    template_name = 'power_grid_organization.html'


class LightingObjectContractInfoDetailView(DetailView):
    model = LightingObjectContractInfo
    template_name = 'contract_info_detail.html'


class ElectricityMeterListView(ListView):
    model = ElectricityMeter
    template_name = 'electricitymeter.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ElectricityMeterFilter(self.request.GET, queryset=self.get_queryset())
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = ElectricityMeter.objects.all().order_by('id')
        return self._filter_group(queryset)

    def _filter_group(self, qs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        else:
            return qs.annotate(short_name=Cast('lighting_object__government__department__area__short_name', CharField())).filter(short_name__in=self.request.user.groups.all().values_list('name'))


class PowerEngineersListView(ListView):
    model = PowerEngineer
    template_name = 'power_engineers.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class AreaListView(ListView):
    model = Area
    template_name = 'area.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class ElectricityMeterDetailView(DetailView):
    model = ElectricityMeter
    template_name = 'electricitymeter_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LocalGovernmentDetailView(DetailView):
    model = LocalGovernment
    template_name = 'government_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class SupplierDetailView(DetailView):
    model = Supplier
    template_name = 'supplier_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LightingObjectNameDetailView(DetailView):
    model = LightingObjectName
    template_name = 'name_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LightingObjectDetailView(DetailView):
    model = LightingObject
    template_name = 'object_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class LightingObjectsListView(ListView):
    model = LightingObject
    template_name = 'objects.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = LightingFilter(self.request.GET, queryset=self.get_queryset())
        return context

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = LightingObject.objects.all().order_by('id')
        return self._filter_group(queryset)

    def _filter_group(self, qs):
        if self.request.user.is_staff or self.request.user.is_superuser:
            return qs
        else:
            return qs.annotate(short_name=Cast('government__department__area__short_name', CharField())).filter(short_name__in=self.request.user.groups.all().values_list('name'))


def upload_locales():
    """
    Функция для загрузки данных по округам
    """
    AREA = {
        'Волоколамский': {
            'Волоколамское':
                [
                    'Волоколамский г.о.'
                ],
            'Лотошинское':
                [
                    'Лотошинский г.о.'
                ],
            'Клинское':
                [
                    'Клин г.о.'
                ],
            'Шаховское':
                [
                    'Шаховская г.о.'
                ]
        },
        'Истринский': {
            'Красногорское':
                [
                    'Красногорск г.о.'
                ],
            'Истринское':
                [
                    'Истра г.о.'
                ],
            'Солнечногорское':
                [
                    'Солнечногорский г.о.'
                ],
            'Одинцовское':
                [
                    'Одинцовский г.о.'
                ]
        },
        'Можайский': {
            'Можайское':
                [
                    'Можайский г.о.'
                ],
            'Рузское':
                [
                    'Рузский г.о.'
                ],
            'Наро-Фоминское':
                [
                    'Наро-Фоминский г.о.'
                ]
        },
        'Домодедовский': {
            'Домодедовское':
                [
                    'г.о. Домодедово',
                    'Ленинский г.о.'
                ],
            'Подольское':
                [
                    'г.о. Подольск'
                ],
            'Чеховское':
                [
                    'г.о. Чехов'
                ],
            'Серпуховское':
                [
                    'г.о. Серпухов',
                    'г.о. Протвино',
                    'г.о. Пущино'
                ],
            'Ступинское':
                [
                    'г.о. Ступино'
                ]
        },
        'Егорьевский': {
            'Егорьевское':
                [
                    'Егорьевск г.о.'
                ],
            'Шатурское':
                [
                    'Шатура г.о.'
                ],
            'Коломенское':
                [
                    'Коломна г.о.'
                ],
            'Воскресенское':
                [
                    'Воскресенск г.о.'
                ],
            'Орехово-Зуевское':
                [
                    'Орехово-Зуево г.о.'
                ]
        },
        'Каширский': {
            'Серебяно-Прудское':
                [
                    'г.о. Серебряные Пруды'
                ],
            'Зарайское':
                [
                    'г.о. Зарайск'
                ],
            'Луховицкое':
                [
                    'г.о. Луховицы'
                ],
            'Озерское':
                [
                    'г.о. Озеры'
                ],
            'Каширское':
                [
                    'г.о. Кашира'
                ]
        },
        'Раменский': {
            'Раменское':
                [
                    'г.о. Раменский',
                    'г.о. Бронницы',
                    'г.о. Жуковский'
                ],
            'Павлово-Посадское':
                [
                    'г.о. Павловский Посад',
                    'г.о. Электрогорск',
                    'г.о. Богородский'
                ],
            'Люберецкое':
                [
                    'г.о. Реутов',
                    'г.о. Люберцы',
                    'г.о. Котельники',
                    'г.о. Лыткарино',
                    'г.о. Дзержинский'
                ],
            'Ногинское':
                [
                    'г.о. Балашиха',
                    'г.о. Черноголовка',
                    'г.о. Электросталь'
                ]
        },
        'Мытищинский': {
            'Мытищинское':
                [
                    'г.о. Мытищи',
                    'г.о. Лобня',
                    'г.о. Химки',
                    'г.о. Долгопрудный'
                ],
            'Пушкинское':
                [
                    'г.о. Пушкинский',
                    'г.о. Королев'
                ],
            'Щелковское':
                [
                    'г.о. Лосино-Петровский',
                    'г.о. Щелково',
                    'г.о. Фрязино'
                ],
            'Сергиево-Посадское':
                [
                    'г.о. Сергиев-Посад'
                ]
        },
        'Дмитровский': {
            'Талдомское':
                [
                    'Талдом г.о.',
                    'Дубна г.о.'
                ],
            'Дмитровское':
                [
                    'Дмитровский г.о.'
                ]
        }
    }

    short_name = 1
    for area, a_value in AREA.items():
        area_obj, created = Area.objects.get_or_create(name=area, short_name=short_name)
        short_name += 1
        for department, d_value in a_value.items():
            department_obj, created = DistrictRoadDepartment.objects.get_or_create(name=department, area=area_obj)
            for government in d_value:
                government_obj, created = LocalGovernment.objects.get_or_create(name=government,
                                                                                department=department_obj)


def get_lighting_object_full_info(lighting_elements):
    """
    Функция для получения данных из БД в нужном формате для последующей загрузки в Excel
    :param lighting_elements:
    :return: Список объектов
    """
    full_info = []
    for lighting in lighting_elements:
        one_element = lighting.get_data_for_excel(lighting)
        full_info.append(one_element)

    return full_info


def export_data_to_excel(request):
    """
    Функция для загрузки данных в Excel
    :param request:
    :return:
    """

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Lightings.xlsx"'

    objects = LightingObject.objects.all()

    df = pd.DataFrame(get_lighting_object_full_info(objects))

    df.to_excel(response, index=False)
    return response
