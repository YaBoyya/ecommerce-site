from django.urls import path

from rest_framework.routers import DefaultRouter

from shopping import views


router = DefaultRouter()
app_name = 'shopping'

router.register('order/item', views.OrderItemsViewSet, basename='order-item')

urlpatterns = router.urls

urlpatterns += [
    path('order/', views.OrderDetailsView.as_view(), name='order'),
    path('cart/', views.CartDetailsView.as_view(), name='cart'),
]
