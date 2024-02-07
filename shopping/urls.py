from django.urls import path

from rest_framework.routers import DefaultRouter

from shopping.views import OrderDetailsView, OrderItemsViewSet


router = DefaultRouter()
app_name = 'shopping'

router.register('order/item', OrderItemsViewSet, basename='item')

urlpatterns = router.urls

urlpatterns += [
    path('order/', OrderDetailsView.as_view(), name='order'),
]
