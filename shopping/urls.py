from django.urls import path

from rest_framework.routers import DefaultRouter

from shopping.views import CartItemViewSet, ShoppingSessionView


router = DefaultRouter()
app_name = 'shopping'

router.register('cart/item', CartItemViewSet, basename='item')

urlpatterns = router.urls

urlpatterns += [
    path('cart/', ShoppingSessionView.as_view(), name='cart'),
]
