from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views


app_name = 'core'
urlpatterns = [
    path('management/product/<str:pk>', views.ProductManagement.as_view(),
         name='product-management'),

    path('index', views.IndexView.as_view(), name='index'),
]

urlpatterns += format_suffix_patterns(urlpatterns)
