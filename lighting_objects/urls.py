from django.urls import path
from .views import *
from django.conf import settings
from django.views.static import serve
from django.conf.urls import *

urlpatterns = [
                  path('export_data_to_excel', export_data_to_excel, name='export_data_to_excel'),

                  path('powerengineers/', PowerEngineersListView.as_view(), name='powerengineers'),

                  path('electricitymeter/', ElectricityMeterListView.as_view(), name='electricitymeter'),
                  path('electricitymeter/<int:pk>/', ElectricityMeterDetailView.as_view(),
                       name='electricitymeter_detail'),

                  path('area/', AreaListView.as_view(), name='area'),

                  path('government/<int:pk>/', LocalGovernmentDetailView.as_view(), name='government_detail'),

                  path('supplier/<int:pk>/', SupplierDetailView.as_view(), name='supplier_detail'),

                  path('name_detail/<int:pk>/', LightingObjectNameDetailView.as_view(), name='name_detail'),

                  path('contract_info_detail/<int:pk>/', LightingObjectContractInfoDetailView.as_view(),
                       name='contract_info_detail'),

                  path('attachmentpoint_detail/<int:pk>/', AttachmentPointDetailView.as_view(),
                       name='attachmentpoint_detail'),
                  path('power_grid_organization/', PowerGridOrganizationListView.as_view(),
                       name='power_grid_organization'),

                  path('details_modal/<int:pk>/', DetailsAjaxView.as_view(), name='details_modal'),

                  path('all_objects/', LightingObjectsListView.as_view(template_name='objects.html'), name='objects'),
                  path('all_objects/<int:pk>/', LightingObjectDetailView.as_view(template_name='object_detail.html'),
                       name='object_detail'),
                  path('', CarouselListView.as_view(template_name='home.html'), name='home'),
                  url(r'^Files/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

              ]
