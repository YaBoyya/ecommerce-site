from django.urls import path

from rest_framework.routers import DefaultRouter

from shopping import views


router = DefaultRouter(trailing_slash=False)
app_name = 'shopping'

router.register('order/item', views.OrderItemsViewSet, basename='order-item')

urlpatterns = router.urls

# TODO add is_active value to orderdetails model to separate profile/order from profile/history
urlpatterns += [
    path('profile/order', views.OrderDetailsView.as_view(), name='order'),
    path('cart', views.CartDetailsView.as_view(), name='cart'),
    path('checkout', views.CheckoutView.as_view(), name='checkout'),
]
